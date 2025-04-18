import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Optional

class WebScraper:
    def __init__(self):
        self.base_urls = [
            'https://www.indiatoday.in/business/market',
            'https://www.moneycontrol.com/news/business/page-{}',
            'https://www.moneycontrol.com/news/business/markets/page-{}',
            'https://www.moneycontrol.com/news/business/stocks/page-{}',
            'https://www.moneycontrol.com/news/business/companies/page-{}',
            'https://www.moneycontrol.com/news/trends/page-{}'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _generate_urls(self) -> List[str]:
        urls = []
        for url in self.base_urls:
            if '{}' in url:
                for i in range(1, 6):  # Pages 1-5
                    urls.append(url.format(i))
            else:
                urls.append(url)
        return urls

    def scrape_content(self, search_word: str) -> Dict[str, List[str]]:
        results = {}
        urls = self._generate_urls()
        
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers, timeout=20)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                elements = soup.find_all(['a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                found_content = []
                
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and re.search(r'\b' + re.escape(search_word) + r'\b', text, re.IGNORECASE):
                        found_content.append(text)
                
                if found_content:
                    results[url] = found_content
                    
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue
                
        return results

    def get_text_content(self, search_word: str) -> Optional[str]:
        scraped_data = self.scrape_content(search_word)
        if not scraped_data:
            return None
            
        all_content = []
        for url, content_list in scraped_data.items():
            all_content.extend(content_list)
            
        return "\n".join(all_content) if all_content else None

# Create a module-level instance for easy import
scraper = WebScraper()
get_text_content = scraper.get_text_content
