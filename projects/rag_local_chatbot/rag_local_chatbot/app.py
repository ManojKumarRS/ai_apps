from fastapi import FastAPI

api = FastAPI(title="RAG Local Chatbot")

@api.get("/health")
def health():
    return {"status": "ok"}

