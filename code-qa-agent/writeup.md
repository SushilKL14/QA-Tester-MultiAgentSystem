
import sys
import os
import shutil
import gradio as gr

PROJECT_ROOT = "/kaggle/working/code-qa-agent"
sys.path.append(PROJECT_ROOT)

SAMPLES_DIR = f"{PROJECT_ROOT}/data/samples"
os.makedirs(SAMPLES_DIR, exist_ok=True)

from src.pipeline import run_pipeline_on_file


def is_dot_noise(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    allowed = set(".·- ")
    return all(c in allowed for c in t)


def format_pretty_output(raw: str) -> str:
    lines = [l.strip() for l in raw.splitlines() if l.strip() and not is_dot_noise(l)]

    if not lines:
        return "⚠ No output"

    full = "\n".join(lines)
    lower = full.lower()

    if "failed" in lower or "error" in lower:
        return "❌ Tests failed\n\n" + full

    if "collected 0 items" in lower:
        return "⚠ No tests found\n\n" + full

    if "passed" in lower:
        return "✔ All tests passed\n\n" + full

    return full


def safe_run(file):
    if file is None:
        return "No file uploaded."

    try:
        if isinstance(file, dict):
            filename = file.get("name", "uploaded.py")
            save_path = os.path.join(SAMPLES_DIR, filename)
            with open(save_path, "wb") as f:
                f.write(file["data"])

        elif hasattr(file, "path"):
            if not os.path.exists(file.path):
                return f"Uploaded file path does not exist: {file.path}"
            save_path = os.path.join(SAMPLES_DIR, file.name)
            shutil.copy(file.path, save_path)

        elif isinstance(file, str):
            if not os.path.exists(file):
                return f"Uploaded file path does not exist: {file}"
            filename = os.path.basename(file)
            save_path = os.path.join(SAMPLES_DIR, filename)
            shutil.copy(file, save_path)

        else:
            return "Invalid file object received."

        result = run_pipeline_on_file(save_path)

        if isinstance(result, dict):
            raw = (
                result.get("stdout")
                or result.get("output")
                or result.get("exec", {}).get("output")
            )
            if raw is None:
                raw = str(result)
        else:
            raw = str(result)

        final_text = format_pretty_output(raw)

        if len(final_text) > 6000:
            final_text = final_text[:6000] + "\n\n...[output truncated]"

        return final_text

    except Exception as e:
        return f"💥 Pipeline crashed: {e}"


ui = gr.Interface(
    fn=safe_run,
    inputs=gr.File(label="Upload Python File (.py)"),
    outputs=gr.Textbox(label="Output", lines=25),
    title="Code QA Tester Agent — Gradio Demo",
)

if __name__ == "__main__":
    ui.launch(share=True)
