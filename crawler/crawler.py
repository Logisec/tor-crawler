import logging
import time
from datetime import datetime
from collections import deque
import threading

class Crawler:
    def __init__(self, tor_client, parser, writer, max_depth=3, max_pages_per_domain=50):
        self.tor_client = tor_client
        self.parser = parser
        self.writer = writer
        self.max_depth = max_depth
        self.max_pages_per_domain = max_pages_per_domain
        
        self.visited_urls = set()
        self.domain_visit_counts = {}
        self.crawl_queue = deque()
        self.results = []
        
        self.lock = threading.Lock()
        
    def should_crawl_url(self, url):
        if url in self.visited_urls:
            return False
            
        domain = self.parser.get_onion_domain(url)
        if not domain:
            return False
            
        if self.domain_visit_counts.get(domain, 0) >= self.max_pages_per_domain:
            logging.info(f"Domain {domain} has reached max pages limit")
            return False
            
        return True
    
    def crawl_page(self, url, depth=0):
        if depth > self.max_depth:
            return None
            
        domain = self.parser.get_onion_domain(url)
        if not domain:
            return None
            
        start_time = time.time()
        
        try:
            logging.info(f"Crawling {url} (depth: {depth})")
            response = self.tor_client.get(url)
            
            if not response:
                return None
                
            response_time = time.time() - start_time
            
            title = self.parser.extract_title(response.text)
            links = self.parser.extract_links(response.text, url)
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'title': title,
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'links_found': len(links)
            }
            
            links_data = []
            for link in links:
                links_data.append({
                    'source_url': url,
                    'target_url': link['url'],
                    'link_text': link['text'],
                    'link_title': link['title'],
                    'timestamp': datetime.now().isoformat()
                })
            
            with self.lock:
                self.visited_urls.add(url)
                self.domain_visit_counts[domain] = self.domain_visit_counts.get(domain, 0) + 1
                
                for link in links:
                    if self.should_crawl_url(link['url']):
                        self.crawl_queue.append((link['url'], depth + 1))
            
            self.writer.write_crawl_data(domain, [result])
            self.writer.write_links_data(domain, links_data)
            
            return result
            
        except Exception as e:
            logging.error(f"Error crawling {url}: {e}")
            return None
    
    def crawl_from_seed(self, seed_url):
        if not self.parser.is_onion_url(seed_url):
            logging.error(f"Invalid .onion URL: {seed_url}")
            return
            
        logging.info(f"Starting crawl from {seed_url}")
        
        self.crawl_queue.append((seed_url, 0))
        
        while self.crawl_queue:
            url, depth = self.crawl_queue.popleft()
            
            if self.should_crawl_url(url):
                result = self.crawl_page(url, depth)
                if result:
                    self.results.append(result)
                    
                time.sleep(3)
            
            if len(self.results) % 10 == 0:
                logging.info(f"Crawled {len(self.results)} pages, {len(self.crawl_queue)} URLs in queue")
        
        logging.info(f"Crawl completed. Total pages crawled: {len(self.results)}")