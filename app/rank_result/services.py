import requests
from bs4 import BeautifulSoup
import random
import tldextract
import base64
from urllib.parse import urlparse, parse_qs
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}" if ext.domain and ext.suffix else url

def find_website_rank_in_results(results, website_url):
    target_domain = extract_domain(website_url)
    print(f"Target domain: {target_domain}")
    for idx, url in enumerate(results, 1):
        result_domain = extract_domain(url)
        print(f"Result {idx}: {url} -> {result_domain}")
        if target_domain == result_domain:
            print(f"Match found at position {idx}")
            return idx
    print("No match found in top results.")
    return None

def extract_bing_real_url(bing_url):
    # If Bing URL has u= param, decode it; else return as-is
    parsed = urlparse(bing_url)
    qs = parse_qs(parsed.query)
    u = qs.get('u')
    if u:
        try:
            decoded = base64.b64decode(u[0]).decode('utf-8')
            return decoded
        except Exception:
            return bing_url
    return bing_url

def scrape_bing_rank(keyword, website_url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.bing.com/"
    }
    urls = []
    for first in [1, 11, 21]:
        url = f"https://www.bing.com/search?q={requests.utils.quote(keyword)}&count=10&first={first}"
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(resp.text, "html.parser")
            for li in soup.select('li.b_algo h2 a'):
                href = li.get('href')
                if href:
                    real_url = extract_bing_real_url(href)
                    urls.append(real_url)
            time.sleep(1)
        except Exception as e:
            continue
    return find_website_rank_in_results(urls, website_url)

def get_rank_result(website_url, keyword, engine=None):
    bing_rank = scrape_bing_rank(keyword, website_url)
    return {
        "website_url": website_url,
        "keyword": keyword,
        "engine": "Bing",
        "rank": bing_rank if bing_rank else "Not found in top 30",
        "last_updated": "just now"
    }
