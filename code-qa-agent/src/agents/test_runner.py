
import tempfile
import subprocess
import sys
import os

def run_pytests(test_code: str, target_file_path: str = ""):
    """
    Run pytest on the generated test code.
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file_path = os.path.join(tmpdir, "generated_test.py")

        # Write the generated test file
        with open(test_file_path, "w") as f:
            f.write(test_code)

        # Ensure user-uploaded module folder is importable
        if target_file_path:
            module_dir = os.path.dirname(os.path.abspath(target_file_path))
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)

        # Execute pytest
        proc = subprocess.run(
            ["pytest", "-q", test_file_path],
            capture_output=True,
            text=True
        )

        return {
            "passed": proc.returncode == 0,
            "output": proc.stdout + "\n" + proc.stderr,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode
        }
