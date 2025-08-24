import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

from langchain_ollama import ChatOllama
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA


DATA_DIR = Path(__file__).resolve().parent.parent / "docs"
CHROMA_DIR = Path(__file__).resolve().parent.parent / ".chroma"
EMBED_MODEL = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")


api = FastAPI(title="RAG Local Chatbot", version="1.0.0")


class IndexResponse(BaseModel):
	documents_indexed: int


class ChatRequest(BaseModel):
	message: str
	k: int = 4
	search_type: str = "similarity"


def build_vector_store() -> Chroma:
	loader = DirectoryLoader(str(DATA_DIR), glob="**/*.txt", loader_cls=TextLoader)
	docs = loader.load()
	splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
	chunks = splitter.split_documents(docs)

	embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
	vector_store = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=str(CHROMA_DIR))
	vector_store.persist()
	return vector_store


def get_vector_store() -> Optional[Chroma]:
	if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
		embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
		return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)
	return None


@api.get("/health")
def health() -> dict:
	return {"status": "ok"}


@api.post("/index")
def index_documents() -> IndexResponse:
	CHROMA_DIR.mkdir(parents=True, exist_ok=True)
	DATA_DIR.mkdir(parents=True, exist_ok=True)
	vs = build_vector_store()
	# Chroma's public API does not expose count directly; use private attr as fallback
	try:
		num = vs._collection.count()  # type: ignore[attr-defined]
	except Exception:
		num = 0
	return IndexResponse(documents_indexed=num)


@api.post("/chat")
def chat(req: ChatRequest = Body(...)) -> dict:
	vector_store = get_vector_store()
	if vector_store is None:
		return {"error": "No vector index found. POST /index after placing .txt files in docs/."}

	retriever = vector_store.as_retriever(search_kwargs={"k": req.k}, search_type=req.search_type)
	llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.1)
	chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
	result = chain.invoke({"query": req.message})
	return {
		"answer": result.get("result"),
		"sources": [getattr(d, "page_content", "") for d in result.get("source_documents", [])],
	}