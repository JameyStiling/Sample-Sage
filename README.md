
# 🎧 Sample Sage

A minimal **FastAPI + Pydantic** scaffold for an MCP-style service that indexes a local **music sample library** and supports **LLM-style queries** (stubbed).

## Quick Start

```bash
# 1) Clone repo, then:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Configure
cp .env.example .env
# (optional) put a few files in ./samples like: pad_dreamscape_Am_88bpm.wav

# 3) Run
uvicorn app.main:app --reload

# 4) Try it
curl http://localhost:8000/healthz
curl -X POST http://localhost:8000/samples/index
curl -X POST http://localhost:8000/samples/query -H "Content-Type: application/json" -d '{"query":"dreamy ambient pads around 90 bpm in A minor"}'
```

## Project Structure

```
app/
  main.py          # FastAPI app + startup
  config.py        # Settings from env
  models.py        # Pydantic schemas
  cache.py         # Simple in-memory cache with TTL
  indexer.py       # Directory scan + filename metadata heuristics
  llm.py           # LLM reasoning (stubbed, pluggable)
  routers/
    health.py      # /healthz
    samples.py     # /samples/*
samples/           # Put .wav/.aiff/.mp3 files here
tests/             # Pytest examples
```

## Notes

- **Pydantic v2** models ensure strict input/output validation.
- **Local cache** avoids expensive rescans; configurable TTL via `.env`.
- **LLM layer** is a stub — implement `LLMClient.match_query(...)` to integrate OpenAI or a local model.
- Designed to be **GitHub-ready** as a starting point for your interview demo.
