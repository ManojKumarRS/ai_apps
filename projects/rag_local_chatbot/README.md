## RAG Local Chatbot (LangChain + Hugging Face Embeddings + Ollama Llama3)

A local RAG service built with FastAPI, using:
- Hugging Face sentence-transformers for embeddings (default: `all-MiniLM-L6-v2`)
- ChromaDB as an embedded vector store
- LangChain RetrievalQA
- Ollama to run `llama3` locally

### Prerequisites
- Install and run Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
- Pull the model: `ollama pull llama3`
- Ensure Python 3.10+

### Install
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Prepare documents
- Put your `.txt` files under `projects/rag_local_chatbot/docs/` (sample files included)

### Run API
```bash
uvicorn rag_local_chatbot.app:api --reload --host 0.0.0.0 --port 8000
```

### Build index
```bash
curl -X POST http://localhost:8000/index
```

### Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"What does ChromaDB do?","k":3}'
```

### Environment overrides
- `EMBED_MODEL` (default `sentence-transformers/all-MiniLM-L6-v2`)
- `OLLAMA_MODEL` (default `llama3`)
