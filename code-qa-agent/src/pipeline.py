    # src/pipeline.py

    import os
    import shutil
    import tempfile
    import subprocess
    from typing import Dict, Any
    from src.agents.code_understanding import analyze_file
    from src.tools.observability import logger


    def _copy_source(code_path: str, tmpdir: str):
        if os.path.isdir(code_path):
            dst = os.path.join(tmpdir, os.path.basename(code_path))
            shutil.copytree(code_path, dst)
            return dst
        else:
            basename = os.path.basename(code_path)
            dst = os.path.join(tmpdir, basename)
            shutil.copy(code_path, dst)
            return dst


    def _run_pytest_in_dir(code_path: str, timeout: int = 30) -> Dict[str, Any]:
        \"\"\"
        Copy code_path into a temp dir and run pytest there.
        If pytest finds no tests, fallback to running the script directly.

        Returns:
            {
                "returncode": int,
                "output": "<stdout + stderr>"
            }
        \"\"\"
        tmpdir = tempfile.mkdtemp(prefix="codeqa_")
        try:
            # Copy file or directory
            if os.path.isdir(code_path):
                test_root = _copy_source(code_path, tmpdir)
            else:
                # Ensure single file starts with test_ so pytest can detect
                basename = os.path.basename(code_path)
                if not basename.startswith("test_"):
                    basename = "test_" + basename
                test_root = os.path.join(tmpdir, basename)
                shutil.copy(code_path, test_root)

            pytest_target = test_root if os.path.isdir(test_root) else tmpdir

            # Run pytest first
            cmd = ["pytest", "-q", pytest_target]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            output = ""
            if proc.stdout:
                output += proc.stdout
            if proc.stderr:
                output += "\\n" + proc.stderr

            # Fallback: if pytest collected 0 items, run as plain Python script
            if "collected 0 items" in output.lower() and os.path.isfile(code_path):
                cmd = ["python", test_root]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                output = ""
                if proc.stdout:
                    output += proc.stdout
                if proc.stderr:
                    output += "\\n" + proc.stderr
                return {"returncode": proc.returncode, "output": output}

            return {"returncode": proc.returncode, "output": output}

        except Exception as e:
            return {"returncode": -1, "output": f"Execution error: {e}"}
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


    def run_pipeline_on_file(save_path: str, run_tests: bool = False) -> Dict[str, Any]:
        \"\"\"
        Primary entrypoint used by the demo app.
        run_tests=False -> only analyze
        run_tests=True  -> analyze AND run pytest
        \"\"\"
        if not os.path.exists(save_path):
            raise FileNotFoundError(save_path)

        try:
            analysis = analyze_file(save_path)
        except Exception as e:
            logger.exception("analyze_file failed")
            return {"error": f"analyze_file failed: {e}"}

        result = {"analysis": analysis}

        if run_tests:
            try:
                exec_res = _run_pytest_in_dir(save_path)
                result["exec"] = exec_res
                result["stdout"] = exec_res.get("output", "")
            except Exception as e:
                logger.exception("Running tests failed")
                result["exec"] = {"returncode": -1, "output": f"Test run failed: {e}"}
                result["stdout"] = result["exec"]["output"]

        return result
