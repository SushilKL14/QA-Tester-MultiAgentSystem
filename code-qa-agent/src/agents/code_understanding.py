# src/agents/code_understanding.py

import os
import ast
import json
from typing import Dict, Any
from src.tools.file_utils import read_file, extract_functions_from_code
from src.tools.observability import logger, timeit
try:
    from src.agents.gemini_client import generate_text
except Exception:
    generate_text = None


def local_infer_function_description(name: str, args: list, src: str) -> str:
    \"\"\"
    Lightweight offline heuristic function documentation.
    \"\"\"
    if name.startswith("test_"):
        return "Unit test function."
    if name.lower() in ("add", "sum", "plus"):
        return "Adds numeric values."
    if name.lower() in ("subtract", "minus", "deduct"):
        return "Subtracts numeric values."
    if len(args) == 0:
        return "Function with no arguments."
    return f"Function operating on args: {', '.join(args)}."


def local_edge_cases(name: str) -> list:
    \"\"\"
    Offline edge-case inference.
    \"\"\"
    if name == "add":
        return ["adding negative numbers", "adding zero", "adding large integers"]
    if name == "subtract":
        return ["subtracting negative numbers", "subtracting zero", "result becomes negative"]
    return ["no special edge cases identified"]


def analyze_with_static_rules(src: str, funcs: dict) -> Dict[str, Any]:
    return {
        "summary": "Static offline analysis — Gemini disabled.",
        "functions": [
            {
                "name": fname,
                "desc": local_infer_function_description(fname, fdata["args"], src),
                "edge_cases": local_edge_cases(fname)
            }
            for fname, fdata in funcs.items()
        ]
    }


@timeit
def analyze_file(path: str) -> Dict[str, Any]:
    src = read_file(path)
    funcs = extract_functions_from_code(src)

    output = {"path": path, "functions": {}}
    for name, node in funcs.items():
        args = [a.arg for a in node.args.args]
        doc = ast.get_docstring(node)
        output["functions"][name] = {"args": args, "doc": doc or ""}

    logger.debug(f"analyze_file -> found {len(funcs)} functions in {path}")

    use_gemini = generate_text and (
        "GEMINI_API_KEY" in os.environ or "GCP_PROJECT" in os.environ
    )

    if use_gemini:
        prompt = (
            "Analyze this Python code and return JSON:\\n"
            "- summary: short file description\\n"
            "- functions: list of {{name, desc, edge_cases[]}}\\n\\n"
            f"Code:\\n{src}"
        )
        try:
            resp = generate_text(prompt)
            resp_text = resp.get("text", "")
            gemini_json = json.loads(resp_text)
            output["gemini"] = gemini_json
        except Exception as e:
            logger.warning(f"Gemini failed: {e}")
            output["gemini"] = analyze_with_static_rules(src, output["functions"])
    else:
        output["gemini"] = analyze_with_static_rules(src, output["functions"])

    return output
