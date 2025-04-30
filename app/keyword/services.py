import random
import requests
from requests.exceptions import RequestException

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

def get_keyword_suggestions(query, regions=['us', 'in', 'uk', 'ca', 'au'], language='en'):
    if not query or len(query.strip()) < 2:
        return ["Please provide a more specific query."]
    
    all_suggestions = []
    random.shuffle(regions)
    
    for region in regions:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}&hl={language}&gl={region}"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()
            
            if len(data) > 1 and isinstance(data[1], list):  # Ensure the response structure is valid
                all_suggestions.extend(data[1])  # Append the suggestions to the list
            else:
                print(f"Unexpected response structure for region {region}")
        except RequestException as e:
            print(f"Failed to fetch data for region {region}: {e}")
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_suggestions))