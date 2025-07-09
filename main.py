import argparse
import logging
import sys
from crawler.tor_client import TorClient 
from crawler.parser import OnionParser
from crawler.file_writer import CrawlDataWriter
from crawler.crawler import Crawler

def setup_logging(log_level='INFO'):
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('crawler.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    parser = argparse.ArgumentParser(description='Tor Hidden Service Crawler for Research')
    parser.add_argument('--start-url', required=True, help='Starting .onion URL to crawl from')
    parser.add_argument('--max-depth', type=int, default=3, help='Maximum crawl depth (default: 3)')
    parser.add_argument('--max-pages', type=int, default=50, help='Maximum pages per domain (default: 50)')
    parser.add_argument('--data-dir', default='data', help='Directory to save crawl data (default: data)')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    
    tor_client = TorClient()
    onion_parser = OnionParser()
    data_writer = CrawlDataWriter(args.data_dir)
    
    crawler = Crawler(
        tor_client=tor_client,
        parser=onion_parser,
        writer=data_writer,
        max_depth=args.max_depth,
        max_pages_per_domain=args.max_pages
    )
    
    try:
        crawler.crawl_from_seed(args.start_url)
    except KeyboardInterrupt:
        logging.info("Crawl interrupted by user")
    except Exception as e:
        logging.error(f"Crawl failed: {e}")
    
    logging.info("Crawler finished")

if __name__ == "__main__":
    main()