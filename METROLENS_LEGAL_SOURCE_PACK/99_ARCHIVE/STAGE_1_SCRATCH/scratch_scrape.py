import urllib.request
import re
import ssl
from urllib.parse import urljoin

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://consumeraffairs.gov.in/pages/legal-metrology-acts"
req = urllib.request.Request(url, headers={"User-agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
        html = response.read().decode("utf-8", errors="ignore")
        links = re.findall(r"href=[\"'](.*?)[\"']", html, re.IGNORECASE)
        with open("scraped_links.txt", "w", encoding="utf-8") as f:
            for link in set(links):
                if ".pdf" in link.lower() or "rules" in link.lower() or "act" in link.lower():
                    f.write(urljoin(url, link) + "\n")
except Exception as e:
    print("Error:", e)
