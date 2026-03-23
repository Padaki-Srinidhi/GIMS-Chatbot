import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

visited = set()
folder = "pages"

# Create folder
os.makedirs(folder, exist_ok=True)

def is_valid(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""

def save_page(url, content):
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filepath = os.path.join(folder, filename + ".txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def crawl(url, base_domain):
    if url in visited:
        return
    
    print("Scraping:", url)
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
    except:
        return

    soup = BeautifulSoup(response.text, "lxml")

    # 🔹 Extract useful content (customize this)
    content = ""
    
    for tag in soup.find_all(["h1", "h2", "h3", "p"]):
        content += tag.get_text(strip=True) + "\n"

    # 🔹 Save page-wise
    save_page(url, content)

    # 🔹 Find internal links
    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])

        if is_valid(full_url, base_domain):
            crawl(full_url, base_domain)


# 🔹 Start
start_url = "https://gimsedu.in/"   # replace with your college site
domain = urlparse(start_url).netloc

crawl(start_url, domain)