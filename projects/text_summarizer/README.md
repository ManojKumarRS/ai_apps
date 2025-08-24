## Text Summarizer API

A minimal FastAPI service that summarizes text using a frequency-based extractive approach. No external ML dependencies.

### Endpoints
- POST `/summarize` — summarize input text with configurable max sentences
- GET `/health` — health probe

### Quickstart
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn text_summarizer.app:api --reload --host 0.0.0.0 --port 8001
```

Example:
```bash
curl -X POST http://localhost:8001/summarize \
  -H 'Content-Type: application/json' \
  -d '{"text":"Sentence one. Sentence two adds more detail. Sentence three is less important.", "max_sentences": 2}'
```
