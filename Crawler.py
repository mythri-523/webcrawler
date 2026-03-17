import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
# ---------------- DOWNLOAD PAGE ----------------
def fetch_page(url):
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            return response.text
        else:
            print("Fetch failed, skipping URL")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None


# ---------------- SAVE HTML ----------------
def save_page(page_number, html):
    if not os.path.exists("pages"):
        os.makedirs("pages")

    filename = f"page_{page_number}.html"
    path = os.path.join("pages", filename)

    with open(path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Saved: {filename}")


# ---------------- EXTRACT LINKS ----------------
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href:
            absolute_url = urljoin(base_url, href)
            links.add(absolute_url)

    print(f"Extracted {len(links)} links")
    return links

# ---------------- CRAWLER LOOP ----------------
def crawl(seed_url, max_pages=5):
    queue = deque()
    visited = set()

    queue.append(seed_url)
    page_count = 0

    while queue and page_count < max_pages:
        current_url = queue.popleft()

        if current_url in visited:
            continue

        html = fetch_page(current_url)
        if not html:
            continue

        page_count += 1
        save_page(page_count, html)

        links = extract_links(html, current_url)
        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)

        visited.add(current_url)
        time.sleep(1)  # politeness delay

    print("\nCrawling Summary")
    print(f"Total pages crawled: {page_count}")
    print(f"Total unique URLs visited: {len(visited)}")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    seed = "https://www.youtube.com/"
    crawl(seed, max_pages=5)