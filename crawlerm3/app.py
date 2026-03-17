import os
import re
import json
import math
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

PAGES_DIR = "pages"
INDEX_FILE = "inverted_index.json"
IDF_FILE = "idf.json"

def extract_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

        # remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        return text

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    return tokens

def main():
    print("Milestone 3 Started\n")

    inverted_index = defaultdict(list)
    document_frequency = defaultdict(int)

    files = os.listdir(PAGES_DIR)
    total_documents = 0

    for file in files:
        if file.endswith(".html"):
            total_documents += 1
            path = os.path.join(PAGES_DIR, file)

            text = extract_text(path)
            tokens = tokenize(text)

            term_frequency = Counter(tokens)

            for word, freq in term_frequency.items():
                inverted_index[word].append((file, freq))
                document_frequency[word] += 1

    # Calculate IDF
    idf = {}
    for word, df in document_frequency.items():
        idf[word] = math.log(total_documents / df)

    # Save inverted index
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, indent=4)

    # Save IDF
    with open(IDF_FILE, "w", encoding="utf-8") as f:
        json.dump(idf, f, indent=4)

    print("Indexing Completed Successfully\n")
    print("Total Documents Indexed:", total_documents)
    print("Total Unique Terms:", len(inverted_index))

    print("\nSample Inverted Index Entries:")
    count = 0
    for word, postings in inverted_index.items():
        print(word, "->", postings)
        count += 1
        if count == 3:
            break

    print("\nSample IDF Values:")
    count = 0
    for word, value in idf.items():
        print(word, "->", round(value, 4))
        count += 1
        if count == 3:
            break

if __name__ == "__main__":
    main()