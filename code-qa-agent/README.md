<h1 align="center">🤖 QA Tester — Multi-Agent Code Analysis</h1>

<p align="center">
  <b>Automated Code Understanding • Test Creation • Execution • Bug Detection</b><br>
  Powered by Modular AI Agents — Offline-friendly with Optional Gemini Enhancements
</p>

---

## 🚀 Project Overview

Modern development wastes too much time writing and updating tests manually.  
This system eliminates that repetitive burden by:

✔ Analyzing Python source code  
✔ Generating runnable unit tests  
✔ Executing and verifying output  
✔ Producing real, actionable bug reports  

All with **zero manual inspection**.

Offline mode ensures this works **securely on any evaluation setup**.  
When allowed, Gemini adds semantic reasoning for deeper insights.

---

## 🧠 System Architecture
```bash
┌────────────────────┐
│ Code Understanding │  → Extract functions + behavior
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Test Generator     │  → Create runnable unit tests
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Test Runner        │  → Execute + capture results
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Bug Reporter       │  → Failures → Defects
└────────────────────┘

```

Each stage passes context — no hallucination, only verifiable execution.

---

## 🧩 Key Features

| Feature | Offline | Gemini-Enhanced |
|--------|:------:|:--------------:|
| Code structure parsing | ✅ | ✅ |
| Semantic function behavior | ⚠ Basic | 🔥 Yes |
| Edge-case inference | Limited | ✔ Strong |
| Test generation | ✔ | ✔ |
| Bug detection | ✔ | ✔ |

No internet? No problem — still fully functional.

---

## 📌 What Problem Does It Solve?

> “Developers spend hours writing tests for simple functions.”

⏱️ Test writing slows delivery  
⚠️ Missing tests hide bugs  
🔄 Refactors require rewriting validation  

This project **automates** what you shouldn’t be doing manually.

---

## 🛠 Tech Stack

- Python
- AST-based static analysis
- PyTest execution engine
- (Optional) Gemini model inference
- Gradio UI demo

---

## 📦 Installation


git clone https://github.com/SushilKL14/QA-Tester-MultiAgentSystem
cd QA-Tester-MultiAgentSystem
pip install -r requirements.txt

▶️ Run the System

1️⃣ Offline Mode (Recommended)

```bash
python src/demo/app.py
```
2️⃣ Gemini-Boosted Mode (Optional)
```bash
export GEMINI_API_KEY="your-key"
USE_GEMINI=true python src/demo/app.py
```

🖥 Live Demo Output (Screenshot)

<img src="https://raw.githubusercontent.com/SushilKL14/QA-Tester-MultiAgentSystem/main/code-qa-agent/demo/imag1.png" width="900" height="400"/>

<img src="https://raw.githubusercontent.com/SushilKL14/QA-Tester-MultiAgentSystem/main/code-qa-agent/demo/imag2.png" width="900" height="400"/>



🧪 Example Output
Number of auto-tests generated

Pass/Fail summary

Traceback for failing tests

Bug report JSON mapping

Every defect is tied to a reproducible failing test — no speculation.

📈 Current Limitations & Future Scope
```bash
| Today                     | Coming Soon                  |
| ------------------------- | ---------------------------- |
| Single-file analysis      | Multi-file relational logic  |
| No async support          | Async + API endpoint testing |
| Basic assertion inference | Learned assertion prediction |

```


👤 Author
SUSHIL
