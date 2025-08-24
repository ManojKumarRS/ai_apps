# ai_apps

Curated, minimal AI application templates you can run locally or extend into production services. Each project is intentionally lightweight and provides clear extension points for your model of choice.

## Projects

1. RAG Local Chatbot
   - Path: `projects/rag_local_chatbot`
   - Offline RAG chatbot scaffold using FastAPI. Ready to integrate Ollama, sentence-transformers, ChromaDB, and LangChain.

2. Text Summarizer API
   - Path: `projects/text_summarizer`
   - Minimal summarization API. Swap in a transformers pipeline or local LLM.

3. Image Captioner API
   - Path: `projects/image_captioner`
   - Minimal image captioning API using base64 input. Replace with your preferred vision-language model.

## Getting Started

Each project contains its own `README.md` and `requirements.txt`. Typical flow:

```bash
cd projects/<project_name>
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m <package>.app
# or
uvicorn <package>.app:api --reload --host 0.0.0.0 --port <port>
```

Where `<project_name>` and `<package>` are the directory and Python package within that project.

## Notes
- Heavy AI dependencies are not pinned or installed by default to keep templates quick to boot. Add them as you wire in models.
- Prefer running models locally through Ollama for privacy and cost control when possible.