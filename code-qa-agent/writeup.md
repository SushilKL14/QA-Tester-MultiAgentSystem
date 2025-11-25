Project Overview
This system automates code analysis, test case generation, execution, and bug reporting using a modular multi-agent design. It operates fully offline but can optionally leverage Gemini for semantic reasoning when allowed. The goal is to reduce human effort in reviewing code and identifying defects.
Problem Statement
Manual unit test writing and validation is slow, inconsistent, and error-prone. Developer velocity drops whenever code changes require test updates. This project solves that by automatically analyzing code behavior and producing executable tests and structured bug findings.
Approach
The architecture follows a pipeline where each agent performs a focused responsibility and passes context to the next stage.
Agent	Responsibility
Code Understanding Agent	Parses code (AST + optional Gemini reasoning) to extract function signatures, behavior, and edge cases
Test Generation Agent	Uses heuristics + model insights to write runnable tests
Test Runner	Executes generated tests and captures results
Bug Reporter	Produces concise defect summaries from failing tests
All communication is stateless across modules except where explicit context is stored.
Offline vs Gemini-Enabled Modes
Mode	Strength	Limitation
Offline (default)	Fully secure, no dependency on external APIs	Only structural insights (syntax-level understanding)
Gemini Assisted	Detects implicit behavior, boundary conditions, failure risks	Requires API key + network access
Fallback ensures the system always functions in restricted evaluation environments.
Key Functionality Demonstrated
•	Source code parsing with abstract syntax trees
•	Classification of extracted functions and parameters
•	Automatic test creation without manual templates
•	Real execution to prove pass/fail truth — not guesswork
•	Defect reporting tied to reproducible test cases
No part of the pipeline pretends to be “smart” where it isn’t — results are based on verifiable execution.
Execution Instructions
pip install -r requirements.txt
python src/demo/app.py     # OFFLINE (recommended for evaluation)
Enable Gemini only if allowed:
export GEMINI_API_KEY="your-key"
USE_GEMINI=true python src/demo/app.py
Test output includes:
•	Test count
•	Pass/fail summary
•	Exact traceback for failures
•	Bug report
Limitations
This MVP is intentionally scoped. It does not:
•	Perform deep flow analysis across module boundaries
•	Confirm logical correctness beyond assertion inference
•	Handle UI or asynchronous code today
These are future improvements, not excuses.
Why This Matters (Impact)
Developers waste excessive time writing test scaffolding instead of solving real problems. This system cuts that overhead immediately, enabling:
•	Faster iteration cycles
•	Higher defect detection earlier
•	More consistent test coverage
If adopted in CI, it scales without extra effort.

