import re
from typing import Dict, List

from fastapi import FastAPI, Body
from pydantic import BaseModel


SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z0-9']+")
STOPWORDS = {
	"the",
	"a",
	"an",
	"to",
	"of",
	"in",
	"and",
	"or",
	"is",
	"are",
	"was",
	"were",
	"be",
	"on",
	"for",
	"with",
	"as",
	"by",
	"at",
}


def split_sentences(text: str) -> List[str]:
	parts = SENTENCE_RE.split(text.strip()) if text else []
	return [p.strip() for p in parts if p.strip()]


def tokenize(text: str) -> List[str]:
	return [t.lower() for t in WORD_RE.findall(text)]


def score_sentences(sentences: List[str]) -> List[float]:
	freq: Dict[str, int] = {}
	for s in sentences:
		for w in tokenize(s):
			if w in STOPWORDS:
				continue
			freq[w] = freq.get(w, 0) + 1

	scores: List[float] = []
	for s in sentences:
		score = 0.0
		for w in tokenize(s):
			if w in STOPWORDS:
				continue
			score += freq.get(w, 0)
		scores.append(score)
	return scores


class SummarizeRequest(BaseModel):
	text: str
	max_sentences: int = 3


api = FastAPI(title="Text Summarizer", version="0.2.0")


@api.get("/health")
def health() -> Dict[str, str]:
	return {"status": "ok"}


@api.post("/summarize")
def summarize(req: SummarizeRequest = Body(...)) -> Dict[str, str]:
	sentences = split_sentences(req.text)
	if not sentences:
		return {"summary": ""}
	scores = score_sentences(sentences)
	ranked_indices = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)
	selected = sorted(ranked_indices[: max(1, req.max_sentences)])
	summary = " ".join(sentences[i] for i in selected)
	return {"summary": summary}