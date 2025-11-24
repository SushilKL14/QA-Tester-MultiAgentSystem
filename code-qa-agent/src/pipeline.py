# src/pipeline.py

"""
End-to-end pipeline invoking the multi-agent flow:
1) Analyze code file
2) Generate tests
3) Run tests
4) Produce bug report (if any)
"""

import os
from src.agents.code_understanding import analyze_file
from src.agents.test_generator import generate_tests_for_file
from src.agents.test_runner import run_pytests
from src.agents.bug_reporter import create_bug_report
from src.tools.observability import logger, metrics


def run_pipeline_on_file(path: str):
    # 1. Analyze
    code_meta = analyze_file(path)

    # 2. Generate tests
    test_code = generate_tests_for_file(code_meta)

    # 3. Run tests
    exec_res = run_pytests(test_code, path)


    metrics["tests_run"] += 1

    if not exec_res["passed"]:
        metrics["tests_failed"] += 1
        report = create_bug_report(exec_res, path)
        logger.warning(f"Generated bug report: {report['title']}")
        return {
            "status": "failed",
            "report": report,
            "exec": exec_res
        }

    else:
        metrics["tests_passed"] += 1
        return {
            "status": "passed",
            "exec": exec_res
        }


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "data/samples/simple_example.py"
    res = run_pipeline_on_file(target)
    print(res)
