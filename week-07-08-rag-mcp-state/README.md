# Week 07 + 08 - RAG, Evidence, MCP & Agent State

## 90 Days of AI Agent Engineering

**Project:** Developer Evidence Assistant

### Goal

Understand how retrieval finds evidence, why an assistant should sometimes decline to
answer, and how MCP and persistent workflow state fit around an application.

### Week 7 - RAG and Evidence

Topics covered:

- Chunking with overlap and source metadata
- Numeric text representations, cosine similarity and top-k vector search
- Citations, insufficient evidence and retrieval failures
- The difference between lexical vectors and learned semantic embeddings

**Implementation:** Search original Markdown learning notes using TF-IDF vectors.
Return the best matching chunk verbatim with its source and chunk ID, or abstain.

**Important:** This is a retrieval-first, extractive baseline. It does not call an LLM,
create learned embeddings, or generate a synthesized answer. Full RAG adds a
generation step grounded in retrieved evidence. TF-IDF is a useful free starting point,
not equivalent to semantic embeddings.

### Week 8 - MCP + Agent State

Topics covered:

- Real MCP client/server communication over stdio
- Exposing a read-only tool and a resource
- Deterministic steps versus LLM-selected actions
- Saving workflow history between program runs

**Implementation:** The optional MCP server exposes `search_documents` and
`learning://guide`. The client initializes a session, lists tools, calls the search
tool, and saves its result. It selects the tool deterministically; no model chooses it.
The ordinary CLI also saves the last 50 question/result records.

History is workflow persistence, **not** semantic memory. Previous answers are not
automatically added to new questions. The JSON store is single-user/single-writer;
simultaneous CLI/client writers may lose an update.

### Architecture

```text
Markdown → overlapping chunks → TF-IDF vectors
Question → cosine search → quoted evidence + citation OR abstention
Result → local JSON history → available after restart

Optional MCP client → stdio MCP server → search_documents → evidence
```

### Project Structure

```text
week-07-08-rag-mcp-state/
├── main.py              # Offline CLI
├── evidence.py          # Chunking, vectors, retrieval and answers
├── state_store.py       # Bounded, atomic history persistence
├── mcp_server.py        # Optional real MCP server
├── mcp_client.py        # Optional real MCP client
├── data/                # Original, public example notes
├── test_evidence.py
├── requirements.txt     # Optional MCP SDK only
├── .gitignore
└── README.md
```

### Run - No Installation Required

In the VS Code PowerShell terminal:

```powershell
cd C:\Users\User\90-days-AI-Agent-Engineer\week-07-08-rag-mcp-state
python main.py --question "What is FastAPI?"
python main.py --question "Who won Wimbledon?"
python main.py --history
python -B -m unittest discover -v
```

Requires Python 3.12+. The default history file is `.state/history.json`
and is ignored by Git. Use `--state path/to/history.json` to choose a different file.
Do not enter private data during a recording.

### Optional MCP Setup

Only do this if you want to install the additional dependency. No AI API key is needed.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python mcp_client.py --question "What is MCP?"
```

The client starts and stops the server automatically. The overall operation has a
30-second deadline and MCP reads have a 15-second timeout. For another MCP-compatible
host, use your virtual environment's Python executable as the command and the absolute
path to `mcp_server.py` as its argument. Never print debug messages on server stdout.

The example follows the official MCP Python SDK **v1** API, bounded below major v2.
The optional SDK was not installed or integration-tested as part of this change.

### Challenges and Bugs

- Initial 80-word chunks made some short queries score below the 0.15 threshold.
  Week 9's evaluation caught this. Using 40 words with 8-word overlap recovered them.
- Matching a word does not prove that a chunk answers a question.
- A citation proves where text came from, not that the text is true.
- Invalid history must produce an error rather than silently overwrite existing work.

### What I Can Explain Now

- Retrieval happens in application code, not magically inside the model.
- TF-IDF vectors measure word overlap; semantic embeddings can match related meanings.
- MCP standardizes communication, not reasoning or autonomous decisions.
- State survives a process restart; context memory requires additional design.

### Mistakes / Things to Watch For

Do not present lexical search as semantic search, history as conversation understanding,
or this extractive demo as a complete generative RAG system. A question such as
"What does FastAPI cost?" can return a FastAPI chunk that does not contain pricing:
this is a useful **retrieval relevance failure** to show in your video.

Retrieved documents are untrusted data. This demo only quotes them; it never executes
their instructions. If you add an LLM, isolate evidence from instructions and validate
citations. No file write tool, arbitrary path reader, shell tool or paid API is exposed.

### YouTube Wrap-Up

**Week 7 title:** What I Learned About RAG and Evidence During My 90-Day AI Engineering Challenge

1. Explain the retrieval → generation boundary (30-60 seconds).
2. Walk through chunking, vectors and the citation format (2-4 minutes).
3. Run a supported question, an unknown question and the pricing failure (2-4 minutes).
4. Explain the short-query bug and the fix (1-2 minutes).
5. Close with MCP and state as the next topic (30-60 seconds).

**Week 8 title:** What I Learned About MCP + Agent State During My 90-Day AI Engineering Challenge

1. Draw client → server → tool.
2. Explain tools versus resources and deterministic versus model-selected actions.
3. If you have installed the SDK, run the MCP client and show tool discovery/results.
4. Run the offline CLI twice and show `--history`.
5. Explain why saved history is not automatically useful memory.

**YouTube links:** Add the actual Week 7 and Week 8 links after publishing.

### Resources

- The supplied 90-Day AI Agent Engineer Master Plan, Weeks 7-8
- MCP Python SDK v1 docs: https://py.sdk.modelcontextprotocol.io/v1/
- MCP Python SDK source examples: https://github.com/modelcontextprotocol/python-sdk/tree/v1.x
- Python JSON: https://docs.python.org/3/library/json.html

### Next Week

Evaluate this evidence assistant on 40 labelled cases and add reliability features.

**Understand what I build, not just make it work.**
