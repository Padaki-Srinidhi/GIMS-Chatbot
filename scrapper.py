import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time

visited = set()
folder = "pages"
os.makedirs(folder, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

MAX_PAGES = 50   # limit crawling

def is_valid(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""

def clean_url(url):
    return url.split("#")[0].rstrip("/")

def save_page(url, content):
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filepath = os.path.join(folder, filename + ".txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def extract_content(soup):
    # ❌ Remove unwanted elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # ✅ Try to get main content area first
    main = soup.find("main") or soup.find("article")

    if main:
        elements = main.find_all(["h1", "h2", "h3", "p", "li"])
    else:
        elements = soup.find_all(["h1", "h2", "h3", "p", "li"])

    content = []

    for el in elements:
        text = el.get_text(strip=True)

        # ✅ Filter noise
        if len(text) > 30:
            content.append(text)

    return "\n".join(content)

def crawl(url, base_domain):
    if len(visited) >= MAX_PAGES:
        return

    url = clean_url(url)

    if url in visited:
        return

    print("Scraping:", url)
    visited.add(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return
    except Exception as e:
        print("Error:", e)
        return

    soup = BeautifulSoup(response.text, "lxml")

    # ✅ Extract clean content
    content = extract_content(soup)

    if content.strip():
        save_page(url, content)

    # 🔹 Extract links
    for link in soup.find_all("a", href=True):
        href = link["href"]

        # ❌ Skip unwanted links
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue

        full_url = urljoin(url, href)
        full_url = clean_url(full_url)

        if is_valid(full_url, base_domain):
            crawl(full_url, base_domain)

    time.sleep(1)  # ✅ prevent blocking


# 🔹 Start
start_url = "https://gimsedu.in/"
domain = urlparse(start_url).netloc

crawl(start_url, domain)

print("✅ Scraping completed. Pages:", len(visited))