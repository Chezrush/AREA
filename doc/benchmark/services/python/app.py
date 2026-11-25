import math
import re

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

PUNCTUATION_RE = re.compile(r"[^\w\s]")
WHITESPACE_RE = re.compile(r"\s+")


class SimilarityRequest(BaseModel):
    text1: str
    text2: str


class SimilarityResponse(BaseModel):
    similarity: float
    interpretation: str


def normalize_text(text: str) -> str:
    lower = text.lower()
    no_punct = PUNCTUATION_RE.sub("", lower)
    clean = WHITESPACE_RE.sub(" ", no_punct)
    return clean.strip()


def generate_frequency_map(words):
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def calculate_tf(unique_words, freq_map, total):
    if total == 0:
        return [0.0] * len(unique_words)
    return [freq_map.get(word, 0) / total for word in unique_words]


def calculate_idf(unique_words, fm1, fm2):
    doc_freq = {}
    for word in unique_words:
        doc_freq[word] = (1 if word in fm1 else 0) + (1 if word in fm2 else 0)
    return [math.log(1.0 + 2.0 / (doc_freq[word] + 1.0)) for word in unique_words]


def calculate_tf_idf(tf, idf):
    return [a * b for a, b in zip(tf, idf)]


def calculate_similarity(tfidf1, tfidf2):
    dot_product = sum(a * b for a, b in zip(tfidf1, tfidf2))
    magnitude1 = math.sqrt(sum(v * v for v in tfidf1))
    magnitude2 = math.sqrt(sum(v * v for v in tfidf2))
    if magnitude1 <= 1e-9 or magnitude2 <= 1e-9:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def interpret_similarity(similarity: float) -> str:
    if similarity <= 0.2:
        return "Dissimilar"
    elif similarity <= 0.4:
        return "Slightly Similar"
    elif similarity <= 0.6:
        return "Moderately Similar"
    elif similarity <= 0.8:
        return "Quite Similar"
    elif similarity <= 1:
        return "Highly Similar"
    return "Unknown"


@app.get("/health")
def health():
    return "ok"


@app.post("/similarity", response_model=SimilarityResponse)
def similarity(req: SimilarityRequest):
    text1 = normalize_text(req.text1)
    text2 = normalize_text(req.text2)

    words1 = text1.split(" ")
    words2 = text2.split(" ")

    fm1 = generate_frequency_map(words1)
    fm2 = generate_frequency_map(words2)

    unique_words = list(set(fm1.keys()) | set(fm2.keys()))

    tf1 = calculate_tf(unique_words, fm1, len(words1))
    tf2 = calculate_tf(unique_words, fm2, len(words2))

    idf = calculate_idf(unique_words, fm1, fm2)

    tfidf1 = calculate_tf_idf(tf1, idf)
    tfidf2 = calculate_tf_idf(tf2, idf)

    sim = calculate_similarity(tfidf1, tfidf2)
    sim = round(sim * 1000) / 1000

    return SimilarityResponse(similarity=sim, interpretation=interpret_similarity(sim))
