from fastapi import FastAPI, Body

api = FastAPI(title="Text Summarizer")

@api.get("/health")
def health():
    return {"status": "ok"}

@api.post("/summarize")
def summarize(text: str = Body(..., embed=True)):
    return {"summary": text[:200]}

