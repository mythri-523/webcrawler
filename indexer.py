import json
import math
import string
from collections import defaultdict

DOCUMENTS = {
    1: {"title": "Python Basics", "content": "Python programming language tutorial"},
    2: {"title": "Machine Learning", "content": "Machine learning uses data and algorithms"},
    3: {"title": "YouTube Tutorials", "content": "YouTube programming tutorials and lessons"},
    4: {"title": "FastAPI Guide", "content": "FastAPI is a Python web framework"},
}

INDEX_FILE = "inverted_index.json"
IDF_FILE = "idf_values.json"
DOCS_FILE = "documents.json"


def tokenize(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.split()


def build_inverted_index(docs):
    N = len(docs)

    raw_counts = defaultdict(lambda: defaultdict(int))

    for doc_id, doc in docs.items():
        tokens = tokenize(doc["title"] + " " + doc["content"])
        for token in tokens:
            raw_counts[token][doc_id] += 1

    inverted_index = {}
    idf_values = {}

    for word, doc_counts in raw_counts.items():

        postings = []

        for doc_id, count in doc_counts.items():
            tokens = tokenize(docs[doc_id]["title"] + " " + docs[doc_id]["content"])
            tf = count / len(tokens)

            postings.append({
                "doc_id": doc_id,
                "tf": tf
            })

        inverted_index[word] = postings

        df = len(doc_counts)
        idf_values[word] = math.log(N / df)

    return inverted_index, idf_values


def save_files(index, idf, docs):

    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

    with open(IDF_FILE, "w") as f:
        json.dump(idf, f, indent=2)

    with open(DOCS_FILE, "w") as f:
        json.dump(docs, f, indent=2)


if __name__ == "__main__":

    inverted_index, idf_values = build_inverted_index(DOCUMENTS)

    save_files(inverted_index, idf_values, DOCUMENTS)

    print("Index created successfully!")