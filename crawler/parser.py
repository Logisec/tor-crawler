from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import urljoin, urlparse

class OnionParser:
    def __init__(self):
        self.onion_pattern = re.compile(r'[a-z2-7]{16,56}\.onion')
        
    def extract_title(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
            return "No title"
        except Exception as e:
            logging.error(f"Error extracting title: {e}")
            return "Parse error"
    
    def extract_links(self, html_content, base_url):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if not href:
                    continue
                    
                absolute_url = urljoin(base_url, href)
                
                if self.is_onion_url(absolute_url):
                    links.append({
                        'url': absolute_url,
                        'text': link.get_text().strip()[:100],
                        'title': link.get('title', '')[:100]
                    })
            
            return links
        except Exception as e:
            logging.error(f"Error extracting links: {e}")
            return []
    
    def is_onion_url(self, url):
        try:
            parsed = urlparse(url)
            return parsed.netloc.endswith('.onion') and self.onion_pattern.search(parsed.netloc)
        except:
            return False
    
    def get_onion_domain(self, url):
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return None