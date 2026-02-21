import requests
import builtwith
from bs4 import BeautifulSoup
import re

class TechDetector:
    def __init__(self, target):
        self.target = target
        if not target.startswith('http'):
            self.url = f'https://{target}'
        else:
            self.url = target
    
    def detect(self):
        result = {
            'url': self.url,
            'web_server': None,
            'frameworks': [],
            'cms': None,
            'javascript_libraries': [],
            'cdn': None,
            'analytics': [],
            'hosting': None
        }
        
        try:
            # Make real HTTP request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10, verify=False, allow_redirects=True)
            
            # Server header
            if 'Server' in response.headers:
                result['web_server'] = response.headers['Server']
            
            # X-Powered-By
            if 'X-Powered-By' in response.headers:
                result['frameworks'].append(response.headers['X-Powered-By'])
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Detect JS libraries
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script['src'].lower()
                if 'jquery' in src:
                    result['javascript_libraries'].append('jQuery')
                if 'react' in src:
                    result['javascript_libraries'].append('React')
                if 'angular' in src:
                    result['javascript_libraries'].append('Angular')
                if 'vue' in src:
                    result['javascript_libraries'].append('Vue.js')
                if 'bootstrap' in src:
                    result['javascript_libraries'].append('Bootstrap')
            
            # Detect CMS
            html_lower = response.text.lower()
            if 'wp-content' in html_lower or 'wordpress' in html_lower:
                result['cms'] = 'WordPress'
            elif 'joomla' in html_lower:
                result['cms'] = 'Joomla'
            elif 'drupal' in html_lower:
                result['cms'] = 'Drupal'
            elif 'shopify' in html_lower:
                result['cms'] = 'Shopify'
            
            # Detect CDN
            if 'cloudflare' in str(response.headers).lower():
                result['cdn'] = 'Cloudflare'
            elif 'akamai' in str(response.headers).lower():
                result['cdn'] = 'Akamai'
            
            # Use builtwith for additional detection
            try:
                tech = builtwith.parse(self.url)
                if 'web-servers' in tech:
                    result['web_server'] = tech['web-servers'][0] if not result['web_server'] else result['web_server']
                if 'web-frameworks' in tech:
                    result['frameworks'].extend(tech['web-frameworks'])
                if 'analytics' in tech:
                    result['analytics'] = tech['analytics']
            except:
                pass
            
            # Remove duplicates
            result['frameworks'] = list(set(result['frameworks']))
            result['javascript_libraries'] = list(set(result['javascript_libraries']))
            
            # Clean empty values
            result = {k: v for k, v in result.items() if v}
            
            if len(result) <= 1:
                return {'error': 'Unable to retrieve technology data'}
            
            return result
            
        except Exception as e:
            return {'error': f'Unable to retrieve data: {str(e)}'}
