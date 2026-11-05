# Build from the repository root; only the two learning folders are copied.
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY week-07-08-rag-mcp-state/evidence.py /app/week-07-08-rag-mcp-state/evidence.py
COPY week-07-08-rag-mcp-state/data/ /app/week-07-08-rag-mcp-state/data/
COPY week-09-10-evaluation-production/agent_loader.py /app/week-09-10-evaluation-production/agent_loader.py
COPY week-09-10-evaluation-production/reliability.py /app/week-09-10-evaluation-production/reliability.py
COPY week-09-10-evaluation-production/main.py /app/week-09-10-evaluation-production/main.py
USER 10001:10001
WORKDIR /app/week-09-10-evaluation-production
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3).close()"]
CMD ["python", "main.py", "--host", "0.0.0.0"]
