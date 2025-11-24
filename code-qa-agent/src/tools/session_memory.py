 # src/tools/session_memory.py
import json
from pathlib import Path
from typing import Dict, Any

MEMORY_FILE = Path("data/memory_bank.json")

def load_memory() -> Dict[str, Any]:
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    return {"recurring_issues": {}}

def save_memory(mem: Dict[str, Any]):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")

def add_recurring_issue(mem: Dict[str, Any], key: str, details: Dict[str, Any]):
    mem.setdefault("recurring_issues", {})
    mem["recurring_issues"].setdefault(key, []).append(details)
    save_memory(mem)
