---
<h1 align="center">🤖 QA Tester — Multi-Agent Code Analysis</h1>

<p align="center">
  Fully Automated Test Generation, Execution & Bug Reporting — Offline First
</p>

---


## 🎯 Project Overview
Unit testing consumes time and slows shipping. This system removes that bottleneck by automating:
✔ Code understanding  
✔ Test case generation  
✔ Test execution  
✔ Bug reporting  

It accelerates developer workflows by eliminating repetitive manual effort while ensuring consistent coverage and early defect discovery.

The system works **fully offline**, making it evaluation-friendly and enterprise-safe. When permitted, **Gemini** can be enabled to infer deeper behavior and edge cases.

---

## ❗ Problem Statement
Manual test writing is:
- Slow and repetitive
- Prone to human oversight
- Painful to maintain as code evolves

This creates delayed feedback loops and decreases product quality.  
Our tool generates tests and identifies defects **instantly**, improving release velocity.

---

## 🧠 System Architecture

Source Code
↓
Code Understanding Agent
↓ (AST + Optional Gemini reasoning)
Test Generation Agent
↓ (Runnable pytest tests)
Test Runner
↓ (Execution results)
Bug Reporter
↓ (Reproducible defect insights)

yaml
Copy code

Each agent performs one focused responsibility — a modular pipeline that scales.

---

## 🔀 Offline vs Gemini Modes

| Mode | Advantage | Limitation |
|------|-----------|------------|
| **Offline (default)** | Secure & self-contained | No implicit behavior detection |
| **Gemini-Assisted** | Smarter scenario inference | Requires internet + API key |

Fallback ensures **robust operation everywhere** (including hackathon restricted networks).

---

## 🚀 Key Features
- Automated test creation using AST analysis
- Executable validation — no hallucinated answers
- Edge case identification
- Structured bug reporting with traceback and repro steps
- CI-friendly modular architecture

Technology is measured by **proof of execution**, not guesswork.

---

## 🖥 Live Demo Output (Screenshot)

<img src="https://raw.githubusercontent.com/SushilKL14/QA-Tester-MultiAgentSystem/main/code-qa-agent/demo/imag1.png" width="650px" height="400"/>

<img src="https://raw.githubusercontent.com/SushilKL14/QA-Tester-MultiAgentSystem/main/code-qa-agent/demo/imag2.png" width="650px" height="400"/>

---

## 🔧 Execution Instructions

### Offline Run (Recommended)

pip install -r requirements.txt
python code-qa-agent/demo/app.py
Enable Gemini (Optional)

```bash
export GEMINI_API_KEY="your-key"
USE_GEMINI=true python code-qa-agent/demo/app.py
```
Output Includes:
Total tests executed

Pass/fail summary

Exact error tracebacks

Complete defect reports

📌 Limitations (Current Version)
To keep MVP scope sharp:

No multi-file inference

No async or UI analysis yet

Does not validate business logic correctness

These gaps are next-stage improvements.

💥 Why This Matters
Testing is a tax on engineering productivity.
Automation here gives:

Faster development cycles

Higher testing coverage with zero manual effort

Consistent early bug detection

Instant CI integration

Engineering teams regain time to solve real problems.
