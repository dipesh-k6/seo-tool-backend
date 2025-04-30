import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def analyze_seo(url):
    response = requests.get(url, timeout=10)
    load_time = response.elapsed.total_seconds()
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL. Status code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.title.string if soup.title and soup.title.string else None
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_desc_tag['content'] if meta_desc_tag and meta_desc_tag.has_attr('content') else None
    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
    images = soup.find_all('img')
    images_with_alt = sum(1 for img in images if img.get('alt'))
    images_without_alt = len(images) - images_with_alt
    word_count = len(soup.get_text().split())
    canonical_tag = soup.find('link', rel='canonical')
    canonical_url = canonical_tag['href'] if canonical_tag and canonical_tag.has_attr('href') else None
    viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
    is_mobile_friendly = bool(viewport_tag)

    # Check for robots.txt and sitemap.xml
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = urljoin(base_url, '/robots.txt')
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        robots_response = requests.get(robots_url, timeout=5)
        has_robots = robots_response.status_code == 200
    except Exception:
        has_robots = False
    try:
        sitemap_response = requests.get(sitemap_url, timeout=5)
        has_sitemap = sitemap_response.status_code == 200
    except Exception:
        has_sitemap = False

    suggestions = []
    if not title_tag:
        suggestions.append('Add a title tag to your page.')
    elif len(title_tag) > 60:
        suggestions.append('Shorten your title tag to under 60 characters.')
    if not meta_description:
        suggestions.append('Add a meta description to improve search visibility.')
    elif len(meta_description) < 50:
        suggestions.append('Make your meta description more descriptive (at least 50 characters).')
    if not h1_tags:
        suggestions.append('Add at least one H1 tag to your page.')
    if len(h1_tags) > 1:
        suggestions.append('Use only one H1 tag per page for best SEO practices.')
    if images_without_alt > 0:
        suggestions.append(f'Add alt text to {images_without_alt} image(s) for better accessibility and SEO.')
    if word_count < 300:
        suggestions.append('Increase your page content to at least 300 words for better SEO.')
    if not canonical_url:
        suggestions.append('Add a canonical tag to specify the preferred URL for this page.')
    if not is_mobile_friendly:
        suggestions.append('Add a viewport meta tag for mobile-friendliness.')
    if not has_robots:
        suggestions.append('Add a robots.txt file to guide search engine crawlers.')
    if not has_sitemap:
        suggestions.append('Add a sitemap.xml file to help search engines index your site.')
    if load_time > 2.5:
        suggestions.append(f'Improve your page load speed (current: {load_time:.2f}s). Aim for under 2.5s.')

    # Placeholders for performance metrics
    performance = {
        'impressions': 'N/A (Connect Google Search Console for data)',
        'visits': 'N/A (Connect Google Analytics for data)',
        'ctr': 'N/A (Connect Google Search Console for data)'
    }

    result = {
        'title': title_tag,
        'meta_description': meta_description,
        'h1_tags': h1_tags,
        'total_images': len(images),
        'images_with_alt': images_with_alt,
        'images_without_alt': images_without_alt,
        'word_count': word_count,
        'canonical_url': canonical_url,
        'is_mobile_friendly': is_mobile_friendly,
        'has_robots_txt': has_robots,
        'has_sitemap_xml': has_sitemap,
        'page_load_time': load_time,
        'suggestions': suggestions,
        'performance': performance,
        'status_code': response.status_code,
        'url': url
    }
    return result
