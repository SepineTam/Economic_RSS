import requests
from bs4 import BeautifulSoup
import logging

def fetch_page(url, http_settings):
    headers = http_settings.get('headers', {})
    timeout = http_settings.get('timeout', 30)
    retries = http_settings.get('retries', 3)

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout, verify=False)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
    
    logging.error(f"Failed to fetch {url} after {retries} attempts")
    return None

def parse_page(html_content, config):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []

    article_list = soup.select(config['selector'])
    for article in article_list:
        parsed_article = {
            'title': article.select_one(config['parsing_rules']['title']).text.strip(),
            'authors': article.select_one(config['parsing_rules']['authors']).text.strip(),
            'abstract': article.select_one(config['parsing_rules']['abstract']).text.strip(),
            'link': article.select_one(config['parsing_rules']['link'])['href']
        }
        articles.append(parsed_article)

    return articles

def scrape_journal(config):
    all_articles = []
    url = config['base_url']
    
    for page in range(config['pagination']['max_pages']):
        html_content = fetch_page(url, config['http_settings'])
        if html_content is None:
            break

        articles = parse_page(html_content, config)
        all_articles.extend(articles)

        if not config['pagination']['enabled']:
            break

        next_page = BeautifulSoup(html_content, 'html.parser').select_one(config['pagination']['next_page_selector'])
        if next_page and 'href' in next_page.attrs:
            url = next_page['href']
        else:
            break

    return all_articles