# v1 Offline Evidence Baseline

## Measured on the development dataset

Dataset: 40 labelled cases (24 supported, 16 unknown).
Runtime: local Python 3.14.4; no API calls, no LLM.

| Metric | Initial: 80-word chunks / 15 overlap | Current: 40-word chunks / 8 overlap |
| --- | ---: | ---: |
| Case pass rate | 35/40 (87.5%) | 40/40 (100%) |
| Retrieval recall@2 | 19/24 (79.2%) | 24/24 (100%) |
| Unknown-question abstention | 16/16 (100%) | 16/16 (100%) |
| API cost | $0 | $0 |

Current observed mean answer latency: 0.051 ms; p95: 0.072 ms.
These are one local run, exclude indexing and network overhead, and vary by machine.
LLM tokens and model tool-selection accuracy are not applicable.

## Failure analysis

Initial supported questions that incorrectly abstained:

- What is RAG?
- Explain chunking
- What are embeddings?
- What are citations?
- What is abstention?

The terms existed in the source. Their cosine scores fell below the 0.15 threshold
because large mixed-topic chunks diluted single-term relevance. Smaller overlapping
chunks recovered these cases. Labels and the 90% evaluation gate were unchanged.

## Remaining failure to show honestly

Try:

```powershell
python ..\week-07-08-rag-mcp-state\main.py --question "What does FastAPI cost?"
```

The lexical matcher returns a FastAPI chunk despite the documents containing no price.
This is **not** a correct answer. A source citation and word overlap do not establish
answer relevance. This pricing example is outside the 40-case development dataset and
shows why 100% on that dataset is not evidence of general accuracy.

## Next evaluation improvements

- Add difficult in-domain unsupported questions to a separately labelled holdout.
- Test synonyms, negation, contradictory sources and malicious document instructions.
- Evaluate answer relevance, evidence sufficiency and citation correctness independently.
- If an LLM is added, record real usage, cost, latency and model-selected tool accuracy.
- Compare lexical retrieval with semantic embeddings before adding complexity.

Reproduce from this directory: `python -B evaluate.py --check`.
