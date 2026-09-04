import urllib.request
import re
import ssl
from urllib.parse import urljoin
from html.parser import HTMLParser

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_href = None
        self.recording = False
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_href = attr[1]
                    self.recording = True
                    self.current_text = ""
                    break

    def handle_data(self, data):
        if self.recording:
            self.current_text += data

    def handle_endtag(self, tag):
        if tag == "a" and self.recording:
            if self.current_href:
                self.links.append((self.current_href, self.current_text.strip()))
            self.recording = False
            self.current_href = None

def get_links(url):
    try:
        req = urllib.request.Request(url, headers={"User-agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            html = response.read().decode("utf-8", errors="ignore")
            parser = LinkParser()
            parser.feed(html)
            return parser.links
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

start_urls = [
    "https://consumeraffairs.gov.in/pages/acts-and-rule",
    "https://consumeraffairs.gov.in/pages/legal-metrology-acts",
    "https://lm.doca.gov.in/",
    "https://consumeraffairs.gov.in/en/acts-and-rules"
]

visited = set()
discovered_pdfs = []

def crawl(url, depth=1):
    if depth > 2 or url in visited: return
    visited.add(url)
    
    links = get_links(url)
    for href, text in links:
        full_url = urljoin(url, href)
        if full_url.lower().endswith(".pdf"):
            if any(keyword in text.lower() or keyword in full_url.lower() for keyword in ["metrology", "packaged", "amendment", "rules", "act"]):
                discovered_pdfs.append((text, full_url, url))
        elif "consumeraffairs.gov.in" in full_url or "lm.doca.gov.in" in full_url:
            if any(k in full_url.lower() or k in text.lower() for k in ["act", "rule", "legal", "metrology"]):
                crawl(full_url, depth + 1)

for su in start_urls:
    crawl(su)

with open("discovered_pdfs.txt", "w", encoding="utf-8") as f:
    for text, full_url, source_url in discovered_pdfs:
        f.write(f"[{text}] -> {full_url} (Found on {source_url})\n")
