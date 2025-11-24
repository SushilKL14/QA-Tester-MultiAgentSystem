# src/tools/file_utils.py
import ast
from typing import List, Dict
import os

def read_file(path: str) -> str:
    """Read file content as text."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_python_files(root: str) -> List[str]:
    """Return list of python files under `root` (non-recursive for demo)."""
    return [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".py")]

def extract_functions_from_code(source: str) -> Dict[str, ast.FunctionDef]:
    """Parse python source and return function name -> ast node."""
    tree = ast.parse(source)
    funcs = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node
    return funcs
