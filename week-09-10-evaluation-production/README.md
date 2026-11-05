# Week 09 + 10 - Agent Evaluation, Reliability & Production Concepts

## 90 Days of AI Agent Engineering

**Project:** Evaluate and harden the Week 7-8 Developer Evidence Assistant.

### Goal

Measure behavior before showing a polished demo, then add a small HTTP delivery layer
with predictable failures and reproducible local setup.

### Week 9 - Agent Evaluation

Topics covered:

- Labelled evaluation datasets, baseline metrics and failure analysis
- Expected status, expected source and expected answer content
- Retrieval recall@2 and unknown-question abstention
- Latency, API cost and honest reporting of unavailable metrics

**Implementation:** Forty original cases: 24 supported questions and 16 out-of-domain
questions. Each case has an ID, expected status, expected source and answer substring.
The evaluator reports pass rate, retrieval recall@2, abstention rate, mean/p95 answer
latency, individual results and failures. `--check` exits nonzero below 90%.

Latency excludes document indexing and the separate retrieval metric query. It is not
end-to-end network latency. API cost is zero because this baseline makes no API calls.
LLM tokens and model tool-selection accuracy are `null`, not invented measurements.

This is a small development dataset, not an independent holdout or proof of production
accuracy. Substring checks are not semantic correctness or a full hallucination test.
The current baseline and known weaknesses are in `BASELINE.md`.

### Week 10 - Reliability + Production Concepts

Topics covered:

- Bounded exponential retries on transient errors only
- Input validation, request size and socket timeouts
- Process-level rate limiting and safe request-ID/latency logs
- Health checks, non-root Docker execution and CI regression checks

**Implementation:** A standard-library HTTP service that reuses Week 7's agent.
It defaults to localhost, accepts only a question field, and returns predictable JSON.
Only timeouts/connection failures are retried (maximum three attempts). The local
retriever normally has no transient network failure; tests inject these failures.

The service fails closed with HTTP 503 after transient retries, rather than inventing
a fallback answer. Unsupported questions return an explicit abstention.

### Architecture

```text
40 labelled cases → shared Week 7 agent → metrics + failure examples

POST /ask → rate/size/type checks → bounded retry → shared evidence agent
         → citation or abstention → JSON response + request ID
GET /health → liveness response
CI → offline tests → evaluation regression gate
```

### Project Structure

```text
week-09-10-evaluation-production/
├── main.py
├── agent_loader.py
├── reliability.py
├── evaluate.py
├── evaluation_cases.json
├── test_production.py
├── BASELINE.md
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

../.github/workflows/weeks-07-10.yml
```

### Run the Evaluation

In VS Code PowerShell:

```powershell
cd C:\Users\User\90-days-AI-Agent-Engineer\week-09-10-evaluation-production
python -B evaluate.py --check
python -B evaluate.py --output evaluation-report.json
python -B -m unittest discover -v
```

Python 3.12+ is required. No dependencies or API keys are needed.
Generated evaluation reports are Git-ignored; the baseline summary is tracked.

### Run the Local API

```powershell
python -B main.py
```

In a second terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
$body = @{question = "What is FastAPI?"} | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType "application/json" -Body $body
```

Use Ctrl+C in the server terminal to stop it.

Responses: 200 for answers/abstentions; 400 invalid input; 404 unknown route;
413 invalid body size; 415 unsupported content type; 429 shared request quota;
503 exhausted transient retries; 500 unexpected application failure.

### Test Both Weeks from the Repository Root

```powershell
cd C:\Users\User\90-days-AI-Agent-Engineer
python -B -m unittest discover -s week-07-08-rag-mcp-state -v
python -B -m unittest discover -s week-09-10-evaluation-production -v
python -B week-09-10-evaluation-production/evaluate.py --check
```

The CI workflow runs these checks on Python 3.12 and 3.14. It does not install or test
the optional MCP dependency. It has not been run on GitHub yet.

### Optional Local Docker Run

Docker Desktop must be running. From the repository root:

```powershell
docker build -f week-09-10-evaluation-production/Dockerfile -t evidence-agent:local .
docker run --rm -p 127.0.0.1:8000:8000 evidence-agent:local
```

The image uses Python 3.12, runs as UID 10001, copies only required source/data, and has
a health check. No secrets or virtual environments are copied. The build may download
a base image. This is a local example, not a deployment instruction.
Docker runtime/build was not tested because Docker Desktop's engine was unavailable.

### Challenges and Bugs

- Evaluation caught poor recall on short questions. Smaller chunks fixed the measured
  cases without changing the labels or relaxing the 90% gate.
- Python 3.14 rejected a literal percent sign in argparse help formatting; using
  "percent" fixed it. A CLI help regression test covers this.
- Putting Week 7 first on the import path shadowed Week 10's `main.py`.
  Keeping Week 10's entry point first fixed the integration tests.
- Retry permanent validation errors? No: retries only make sense for transient failures.

### What I Can Explain Now

- Unit tests check individual behavior; evaluation measures behavior across examples.
- A high benchmark score is only meaningful relative to the dataset.
- Retries must be bounded and should not repeat unsafe side effects.
- Liveness means the service responds, not that every answer is useful.
- A request ID links events without logging user questions.

### Mistakes / Things I Must Not Claim

This is **production-oriented learning**, not a production-ready service:
there is no authentication, authorization, TLS, distributed quota, database, semantic
embedding model, LLM integration, distributed tracing, or multi-worker concurrency.
The server is single-threaded, with a five-second per-socket timeout, not an overall
request deadline. Its 20-requests-per-60-seconds quota is shared across all clients and
resets on restart. Health only checks liveness, not evidence quality.

Keep the default localhost binding. Do not expose the service publicly. Real public
deployment requires an authenticated reverse proxy, total deadlines, robust server,
authorization and user isolation; these are concepts to study, not features implemented
here. No existing auth or backend API was changed.

### YouTube Wrap-Up

**Week 9 title:** What I Learned About Agent Evaluation During My 90-Day AI Engineering Challenge

1. Explain why "it worked once" is not a quality measure.
2. Show the 40 labelled examples and explain the metrics.
3. Run the evaluator and show the original short-query failures in `BASELINE.md`.
4. Demonstrate "What does FastAPI cost?" as a remaining relevance failure.
5. Explain why this tiny dataset needs harder examples and a holdout.

**Week 10 title:** What I Learned About Reliability + Production During My 90-Day AI Engineering Challenge

1. Compare the CLI prototype with the HTTP wrapper.
2. Start the API, check health and send a valid request.
3. Send an empty question and show the validation error.
4. Show retry/error tests, the Dockerfile and CI workflow.
5. Explain what is still needed before public deployment.

**YouTube links:** Add the actual Week 9 and Week 10 links after publishing.

### Resources

- The supplied 90-Day AI Agent Engineer Master Plan, Weeks 9-10
- Python unittest: https://docs.python.org/3/library/unittest.html
- Python http.server: https://docs.python.org/3/library/http.server.html
- Docker Python guide: https://docs.docker.com/guides/python/
- GitHub Actions Python guide: https://docs.github.com/en/actions/tutorials/build-and-test-code/python

### Next Week

Design the capstone: problem, users, architecture, acceptance criteria and evaluation
plan. Do not confuse this free learning demo with the final paid capstone.

**Learn → Attempt → Break → Debug → Understand → Build → Document**
