import csv
import os
import re
import logging

class CrawlDataWriter:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def sanitize_filename(self, onion_domain):
        safe_name = re.sub(r'[^\w\-_.]', '_', onion_domain.replace('.onion', ''))
        return f"{safe_name}.csv"
    
    def write_crawl_data(self, onion_domain, crawl_results):
        filename = self.sanitize_filename(onion_domain)
        filepath = os.path.join(self.data_dir, filename)
        
        file_exists = os.path.exists(filepath)
        
        try:
            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'url', 'title', 'status_code', 'response_time', 'links_found']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                for result in crawl_results:
                    writer.writerow(result)
                    
            logging.info(f"Wrote {len(crawl_results)} records to {filepath}")
            
        except Exception as e:
            logging.error(f"Error writing to {filepath}: {e}")
    
    def write_links_data(self, onion_domain, links_data):
        filename = f"links_{self.sanitize_filename(onion_domain)}"
        filepath = os.path.join(self.data_dir, filename)
        
        file_exists = os.path.exists(filepath)
        
        try:
            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['source_url', 'target_url', 'link_text', 'link_title', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                for link in links_data:
                    writer.writerow(link)
                    
        except Exception as e:
            logging.error(f"Error writing links to {filepath}: {e}")