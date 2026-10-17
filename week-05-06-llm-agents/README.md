# Week 05 + 06 - LLM Application Fundamentals & Tool Calling

## 90 Days of AI Agent Engineering

**Project:** AI Resume Analyzer Agent

This project combines Week 5 and Week 6 into one Python application to demonstrate how LLM applications generate structured results and how agents interact with Python tools.

### Week 5 - LLM Application Fundamentals

Topics covered:

- LLM requests and messages
- System and user roles
- Tokens and context
- Prompting
- Structured outputs
- Pydantic validation
- Latency and cost considerations
- Model/application boundaries

**Implementation:** Send a sample resume and job description to an LLM and return validated structured results containing skills, strengths, missing skills, and recommendations.

### Week 6 - Tool Calling and Agent Loops

Topics covered:

- Tool definitions and JSON schemas
- LLM tool selection
- Python function execution
- Tool allowlisting and argument validation
- Agent execution loops
- Error handling
- Termination conditions

**Implementation:** A manual agent loop that allows an LLM to request a Python function for calculating skill overlap.

### Architecture

**Week 5**

Resume + Job Description → LLM → Structured Output → Pydantic Validation → Result

**Week 6**

User Input → LLM → Tool Request → Python Function → Tool Result → LLM → Final Response

### Project Structure

```text
week-05-06-llm-agents/
├── main.py
├── llm_client.py
├── schemas.py
├── tools.py
├── agent.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create `.env` from `.env.example` and supply an API key.

Run:

```powershell
python main.py
```

### Key Takeaways

**Week 5:** An LLM application is more than a prompt. The surrounding application must manage requests, validate results, handle failures, and consider token usage, latency and cost.

**Week 6:** The LLM does not directly execute Python code. It requests a tool, and the application decides whether and how to execute that tool.

### Limitations

- This is an educational demonstration, not a production resume screening service.
- Skill matching uses simple case-insensitive keyword overlap.
- The overlap percentage is not an ATS score or a measure of candidate suitability.
- The project uses a fictional resume.
- It does not implement persistent storage, authentication or production-grade retries.

### Learning Philosophy

**Understand what I build not just make it work.**

Learn → Attempt → Break → Debug → Understand → Build → Document.