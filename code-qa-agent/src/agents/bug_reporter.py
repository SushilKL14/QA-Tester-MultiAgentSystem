# src/agents/bug_reporter.py

"""
Bug Reporter Agent
- Takes failing test output and produces a human-readable bug report
- Optionally formats it for Jira/GitHub issues (simulated)
"""

from typing import Dict
from src.tools.session_memory import load_memory, add_recurring_issue
from src.tools.observability import logger


def parse_pytest_output(output: str) -> Dict:
    """
    Very naive parsing for demo.
    Returns last 20 lines of pytest output.
    """
    return {"summary": output.splitlines()[-20:]}


def create_bug_report(exec_summary: Dict, source_path: str) -> Dict:
    parsed = parse_pytest_output(exec_summary["output"])
    report = {
        "title": f"Auto-generated bug report for {source_path}",
        "description": "\n".join(parsed["summary"]),
        "severity": "medium",
        "suggested_fix": "Investigate failing assertion in generated tests.",
    }

    mem = load_memory()
    add_recurring_issue(mem, source_path, {"report": report})

    logger.info("Created bug report and saved to memory bank.")
    return report
