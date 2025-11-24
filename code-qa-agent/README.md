🚀 Code-QA-Agent
A Multi-Agent Automated System for Code Understanding, Test Generation, Test Execution, and Bug Reporting
This project implements a multi-agent architecture that analyzes Python files, generates tests, runs them in isolation, and produces structured bug reports.
The system exposes a Gradio interface for easy interaction and demonstration.

🔍 1. Problem the Project Solves
Manually reviewing Python code is slow and inconsistent. Developers need:
•	Automated understanding of unfamiliar code.
•	Automatic generation of meaningful test cases.
•	On-the-fly execution of tests.
•	Clear, structured reports summarizing issues.
This project solves that by using four cooperative agents that process any uploaded Python file end-to-end.

🧠 2. Solution Summary
The system contains a multi-agent pipeline:
Agent 1: Code Understanding Agent
Analyzes the file and extracts:
•	Functions
•	Parameters
•	Expected behaviors
•	Logical flow
•	Potential edge cases
Agent 2: Test Generator Agent
Uses the understanding from Agent 1 to generate:
•	Unit tests (PyTest)
•	Boundary tests
•	Negative tests
•	Edge-case scenarios
Agent 3: Test Runner Agent
Executes the generated tests inside a safe temporary workspace:
•	Captures stdout / stderr
•	Detects failures
•	Sanitizes noise from PyTest output
Agent 4: Bug Reporter Agent
Creates a clean report:
•	Summary
•	What passed / failed
•	Potential root cause
•	Suggestions for fixes
Everything flows through src/pipeline.py, which orchestrates the agents.














🏗 3. Project Structure
code-qa-agent/
├─ data/
│  ├─ samples/                 # sample repos / code files for demo
├─ notebooks/
│  ├─ demo_notebook.ipynb
├─ src/
│  ├─ agents/
│  │  ├─ code_understanding.py
│  │  ├─ test_generator.py
│  │  ├─ test_runner.py
│  │  └─ bug_reporter.py
│  ├─ tools/
│  │  ├─ file_utils.py
│  │  ├─ session_memory.py
│  │  └─ observability.py
│  ├─ pipeline.py
├─ demo/
│  ├─ streamlit_app.py
├─ tests/                      # unit tests for the agent code itself
├─ .github/
│  ├─ workflows/ci.yaml        # optional CI example
├─ README.md
├─ requirements.txt
└─ writeup.md
🎛 4. Demo Application (Gradio)
The UI is built in demo/app.py with the following features:
✔ Upload any .py file
✔ Pipeline runs automatically
✔ Pretty-formatted output
✔ Handles PyTest noise / long outputs
✔ Detects failures and missing tests
✔ Shows final agent result clearly
This is your actual logic:
•	safe_run() handles:
o	file saving
o	pipeline execution
o	formatting
o	crash protection
•	format_pretty_output() cleans PyTest noise
•	Output is shown via a large textbox
To launch:
python demo/app.py
Kaggle automatically forces share=True, so the UI will get a public link.

⚙ 5. Installation
1. Clone repo
git clone https://github.com/your-username/code-qa-agent.git
cd code-qa-agent
2. Install dependencies
pip install -r requirements.txt
3. Run the demo
python demo/app.py

🧪 6. How the Multi-Agent Pipeline Works
Step-by-Step Execution Flow
1.	User uploads a file → app.py saves it
2.	pipeline.py reads the file
3.	Code Understanding Agent extracts structure
4.	Test Generator Agent creates tests
5.	Test Runner Agent runs PyTest safely
6.	Bug Reporter Agent summarizes all results
7.	UI displays the cleaned final output

📌 7. Example Output (Realistic)
✔ All tests passed

Generated Tests:
- test_add_positive_numbers
- test_add_negative_numbers
- test_add_zero

Execution Report:
3 passed, 0 failed in 0.01s
Or a failed case:
❌ Tests failed

FAILED test_file.py::test_divide_by_zero
ZeroDivisionError: division by zero

Suggested Fix:
Add input validation for divisor == 0

📚 8. Key Concepts Used (for scoring)
Your project clearly demonstrates:
✔ Multi-Agent Architecture
(distinct agents with separate responsibilities)
✔ Memory & Session Tracking
(session_memory.py maintains persistent pipeline state)
✔ Observability
(custom logs + execution traces)
✔ Code Understanding & Reasoning
(the understanding agent analyzes AST-level information)
✔ Automated Test Generation
(logic-driven PyTest file creation)
✔ Sandbox Test Execution
(runs tests inside temporary directories)
✔ Front-end Integration (Gradio)
(interactive uploader + output formatting)
This checks all requirements for the "Implementation" category.

🧾 9. File: writeup.md
You should summarize:
•	architecture
•	decisions
•	agent roles
•	pipeline flow
•	screenshots of UI
•	example output
Keep it concise, technical, and architecture-driven.

🔐 10. Security Note
This project never stores API keys, and is safe for evaluation.

🏁 11. Conclusion
This project demonstrates:
•	solid multi-agent design
•	automated code reasoning
•	test generation
•	reliable test execution
•	clean UI
•	strong engineering structure
Everything is modular, testable, and easy to extend.

