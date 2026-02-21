import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DynamicCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.endpoints = []
        self.domain = urlparse(base_url).netloc
    
    def crawl(self, max_depth=2, max_pages=20):
        """
        Dynamic crawler that discovers endpoints through:
        - Static HTML parsing
        - JavaScript-rendered content
        - Form discovery
        - AJAX endpoint detection
        """
        
        # Static crawling
        self._static_crawl(self.base_url, depth=0, max_depth=max_depth, max_pages=max_pages)
        
        # Dynamic crawling with Selenium (headless)
        try:
            self._dynamic_crawl(self.base_url, max_pages=min(5, max_pages))
        except:
            pass  # Fallback to static only if Selenium fails
        
        return self.endpoints
    
    def _static_crawl(self, url, depth, max_depth, max_pages):
        if depth > max_depth or len(self.visited) >= max_pages:
            return
        
        if url in self.visited:
            return
        
        self.visited.add(url)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            if response.status_code != 200:
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract endpoint info
            endpoint = {
                'url': url,
                'method': 'GET',
                'parameters': self._extract_url_params(url),
                'forms': self._extract_forms(soup, url),
                'links': []
            }
            
            self.endpoints.append(endpoint)
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                # Only crawl same domain
                if urlparse(full_url).netloc == self.domain:
                    endpoint['links'].append(full_url)
                    self._static_crawl(full_url, depth + 1, max_depth, max_pages)
        
        except:
            pass
    
    def _dynamic_crawl(self, url, max_pages=5):
        """
        Use Selenium to discover JavaScript-rendered content
        """
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(10)
            
            driver.get(url)
            time.sleep(2)  # Wait for JS to execute
            
            # Get dynamically loaded content
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find AJAX endpoints by monitoring network
            # (This is simplified - real implementation would use browser DevTools Protocol)
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Look for fetch/axios/XMLHttpRequest patterns
                    content = script.string
                    if any(keyword in content for keyword in ['fetch(', 'axios.', 'XMLHttpRequest', '$.ajax', '$.get', '$.post']):
                        # Extract potential endpoints (simplified)
                        import re
                        urls = re.findall(r'["\']([/\w\-\.]+)["\']', content)
                        for potential_url in urls:
                            if potential_url.startswith('/'):
                                full_url = urljoin(self.base_url, potential_url)
                                if full_url not in self.visited:
                                    self.endpoints.append({
                                        'url': full_url,
                                        'method': 'GET',
                                        'parameters': [],
                                        'forms': [],
                                        'links': [],
                                        'source': 'dynamic'
                                    })
            
            driver.quit()
            
        except:
            pass
    
    def _extract_url_params(self, url):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return [{'name': k, 'value': v[0] if v else ''} for k, v in params.items()]
    
    def _extract_forms(self, soup, base_url):
        forms = []
        
        for form in soup.find_all('form'):
            action = form.get('action', '')
            method = form.get('method', 'GET').upper()
            
            form_url = urljoin(base_url, action) if action else base_url
            
            inputs = []
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_name = input_tag.get('name')
                input_type = input_tag.get('type', 'text')
                
                if input_name:
                    inputs.append({
                        'name': input_name,
                        'type': input_type,
                        'value': input_tag.get('value', '')
                    })
            
            forms.append({
                'action': form_url,
                'method': method,
                'inputs': inputs
            })
        
        return forms
