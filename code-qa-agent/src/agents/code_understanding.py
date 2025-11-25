# src/agents/code_understanding.py

"""
Code Understanding Agent
- Reads file(s)
- Extracts functions and docstrings
- Produces a structured representation of code units to test"""
from src.agents.gemini_client import generate_text
import json

from typing import Dict, Any
from src.tools.file_utils import read_file, extract_functions_from_code
from src.tools.observability import logger, timeit

@timeit
def analyze_file(path: str) -> Dict[str, Any]:
    src = read_file(path)
    funcs = extract_functions_from_code(src)
    
    # Existing AST extraction
    output = {"path": path, "functions": {}}
    for name, node in funcs.items():
        args = [a.arg for a in node.args.args]
        import ast
        doc = ast.get_docstring(node)
        output["functions"][name] = {"args": args, "doc": doc or ""}

    logger.debug(f"analyze_file -> found {len(funcs)} functions in {path}")

    # Gemini reasoning
    prompt = f"""
You are a Python code analyst. Summarize this file in JSON with:
- summary: short description
- functions: list of {{'name','desc'}}
- edge_cases: potential edge cases for each function
Code:
