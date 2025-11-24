# src/agents/code_understanding.py
"""
Code Understanding Agent
- Reads file(s)
- Extracts functions and docstrings
- Produces a structured representation of code units to test"""
from typing import Dict, Any
from src.tools.file_utils import read_file, extract_functions_from_code
from src.tools.observability import logger, timeit

@timeit
def analyze_file(path: str) -> Dict[str, Any]:
    src = read_file(path)
    funcs = extract_functions_from_code(src)
    output = {"path": path, "functions": {}}
    for name, node in funcs.items():
        # For each function we extract argument names and docstring (if present)
        args = [a.arg for a in node.args.args]
        # docstring AST helper
        import ast
        doc = ast.get_docstring(node)
        output["functions"][name] = {"args": args, "doc": doc or ""}
    logger.debug(f"analyze_file -> found {len(funcs)} functions in {path}")
    return output
