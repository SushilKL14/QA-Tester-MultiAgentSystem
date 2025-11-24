import sys, os, json

PROJECT_ROOT = "/kaggle/working/code-qa-agent"
sys.path.append(PROJECT_ROOT)

SAMPLES_DIR = f"{PROJECT_ROOT}/data/samples"
os.makedirs(SAMPLES_DIR, exist_ok=True)

import gradio as gr
from src.pipeline import run_pipeline_on_file


def runner(file):
    if file is None:
        return "Error: No file uploaded."

    path = f"{SAMPLES_DIR}/{file.name}"
    with open(path, "wb") as f:
        f.write(file.read())

    result = run_pipeline_on_file(path)

    # RETURN STRING instead of dict → prevents Gradio schema bug
    return json.dumps(result, indent=2)


ui = gr.Interface(
    fn=runner,
    inputs=gr.File(label="Upload Python File (.py)"),
    outputs=gr.Textbox(label="Pipeline Output", lines=20),
    title="Code QA Tester Agent — Gradio Demo"
)

ui.launch(share=True)

