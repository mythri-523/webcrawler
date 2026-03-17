import json
import os
import string
from collections import defaultdict
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

INDEX_FILE = "inverted_index.json"
IDF_FILE = "idf_values.json"
DOCS_FILE = "documents.json"


def load_files():

    with open(INDEX_FILE) as f:
        inverted_index = json.load(f)

    with open(IDF_FILE) as f:
        idf_values = json.load(f)

    with open(DOCS_FILE) as f:
        documents = json.load(f)

    return inverted_index, idf_values, documents


inverted_index, idf_values, DOCUMENTS = load_files()


def tokenize(text):

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.split()


def search(query):

    tokens = tokenize(query)

    scores = defaultdict(float)

    for word in tokens:

        if word in inverted_index:

            idf = idf_values[word]

            for posting in inverted_index[word]:

                doc_id = str(posting["doc_id"])
                tf = posting["tf"]

                scores[doc_id] += tf * idf

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    results = []

    for doc_id, score in ranked:

        doc = DOCUMENTS[doc_id]

        results.append({
            "title": doc["title"],
            "score": round(score, 3)
        })

    return results


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/search")
def search_endpoint(q: str = Query(...)):

    return {
        "query": q,
        "results": search(q)
    }