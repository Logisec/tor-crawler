import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import logging

class TorClient:
    def __init__(self, proxy_host='127.0.0.1', proxy_port=9050, timeout=30):
        self.session = requests.Session()
        
        self.session.proxies = {
            'http': f'socks5h://{proxy_host}:{proxy_port}',
            'https': f'socks5h://{proxy_host}:{proxy_port}'
        }
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.timeout = timeout
        self.last_request_time = 0
        self.min_delay = 2
        
    def get(self, url, **kwargs):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        
        try:
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            self.last_request_time = time.time()
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return None