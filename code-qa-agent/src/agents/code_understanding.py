# src/agents/code_understanding.py

"""
Code Understanding Agent
- Reads file(s)
- Extracts functions and docstrings
- Produces a structured representation of code units to test
"""
from typing import Dict, Any
from src.tools.file_utils import read_file, extract_functions_from_code
from src.tools.observability import logger, timeit
from src.agents.gemini_client import generate_text
import json
import ast

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

    # Ask Gemini for higher-level reasoning
    prompt = (
        "Analyze this Python code and return JSON:\n"
        "- summary: short file description\n"
        "- functions: list of {name, desc, edge_cases[]}\n\n"
        f"Code:\n{src}"
    )

    gemini_response = generate_text(prompt)

    try:
        gemini_json = json.loads(gemini_response)
    except json.JSONDecodeError:
        logger.error("Gemini responded with non-JSON text")
        gemini_json = {"summary": "", "functions": []}

    output["gemini"] = gemini_json
    return output
