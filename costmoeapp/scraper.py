import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import scrapy
from scrapy.crawler import CrawlerProcess
import time
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraper:
    def __init__(self, use_selenium=False):
        self.use_selenium = use_selenium
        
        # Selenium configuration (optional)
        if self.use_selenium:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=Service("chromedriver"), options=options)
    
    def fetch_static_page(self, url):
        """Fetches static pages using Requests and BeautifulSoup."""
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
    
    def fetch_dynamic_page(self, url):
        """Fetches dynamic pages using Selenium."""
        if not self.use_selenium:
            return None
        try:
            self.driver.get(url)
            time.sleep(3)  # Allow JavaScript to load
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            logging.error(f"Selenium error fetching {url}: {e}")
            return None
    
    def scrape_shopee(self):
        """Scraping Shopee Philippines using BeautifulSoup."""
        url = "https://shopee.ph"
        soup = self.fetch_static_page(url)
        if soup:
            return [item.text.strip() for item in soup.find_all('div', class_='shopee-item-card')]
        return []

    def scrape_lazada(self):
        """Scraping Lazada Philippines using Selenium."""
        url = "https://www.lazada.com.ph"
        soup = self.fetch_dynamic_page(url)
        if soup:
            return [item.text.strip() for item in soup.find_all('div', class_='product-title')]
        return []

    def scrape_all(self):
        """Scrapes all supported e-commerce websites and logs the process."""
        logging.info("Starting full website scraping...")
        results = {
            "shopee": self.scrape_shopee(),
            "lazada": self.scrape_lazada(),
            # Additional site-specific methods can be added here
        }
        logging.info("Scraping completed successfully.")
        return results

    def close(self):
        """Closes Selenium driver if used."""
        if self.use_selenium:
            self.driver.quit()

# Scrapy Spider Example
class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    start_urls = ['https://www.amazon.com/s?k=laptop']
    
    def parse(self, response):
        for product in response.css('div.s-main-slot div.s-result-item'):
            yield {
                'title': product.css('span.a-text-normal::text').get(),
                'price': product.css('span.a-price-whole::text').get(),
            }

if __name__ == "__main__":
    scraper = WebScraper(use_selenium=True)
    data = scraper.scrape_all()
    print(data)
    scraper.close()
    
    # Running Scrapy for large-scale data extraction
    process = CrawlerProcess()
    process.crawl(AmazonSpider)
    process.start()
