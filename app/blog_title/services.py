import requests
from bs4 import BeautifulSoup
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

def scrape_google_titles(query, results):
    try:
        url = f"https://www.google.com/search?q={query}+blog+titles"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        titles = [g.text for g in soup.find_all('h3')][:5]
        results.extend(titles)
    except Exception as e:
        print(f"Google scraping error: {e}")

def scrape_bing_titles(query, results):
    try:
        url = f"https://www.bing.com/search?q={query}+blog+titles"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.bing.com/"
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        titles = [b.text for b in soup.find_all('h2')][:5]
        results.extend(titles)
    except Exception as e:
        print(f"Bing scraping error: {e}")

def generate_smart_titles(query):
    templates = [
        f"Top 10 {query.title()} Tips You Should Know",
        f"Ultimate Guide to {query.title()}",
        f"{query.title()} Secrets: What Experts Don't Tell You",
        f"Everything You Need to Know About {query.title()}",
        f"Frequently Asked Questions About {query.title()}",
        f"The Pros and Cons of {query.title()}",
        f"Common Myths About {query.title()}",
    ]
    random.shuffle(templates)
    return templates

def get_blog_titles(query):
    if not query or len(query.strip()) < 2:
        return ["Please provide a more specific blog topic."]
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        response = requests.get(url, headers=headers, timeout=5)
        suggestions = []
        if response.status_code == 200:
            suggestions = response.json()[1][:4]
        templates = [
            f"Top 10 {query.title()} Tips You Should Know",
            f"The Latest Research on {query.title()}",
            f"{query.title()} Secrets: What Experts Don't Tell You",
            f"Everything You Need to Know About {query.title()}",
            f"Frequently Asked Questions About {query.title()}",
            f"The Pros and Cons of {query.title()}",
            f"Common Myths About {query.title()}"
        ]
        template_titles = random.sample(templates, 2)
        titles = suggestions + template_titles
        random.shuffle(titles)
        if not titles or all(not t for t in titles):
            return ["No suggestions found. Try a different topic."]
        return titles
    except Exception as e:
        return [f"Error: {str(e)}"]
