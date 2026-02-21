import requests
import random
import string

class ReflectionTester:
    def __init__(self):
        # Harmless unique tokens for reflection detection
        self.token_prefix = 'XGENIE'
    
    def generate_token(self):
        """Generate unique harmless token"""
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f'{self.token_prefix}{random_str}'
    
    def test_reflections(self, attack_surface):
        """
        Test each parameter for reflection using harmless tokens
        """
        results = []
        
        for surface in attack_surface:
            token = self.generate_token()
            
            try:
                if surface['method'] == 'GET':
                    reflected = self._test_get(surface, token)
                else:
                    reflected = self._test_post(surface, token)
                
                if reflected:
                    results.append({
                        'url': surface['url'],
                        'method': surface['method'],
                        'parameter': surface['parameter'],
                        'token': token,
                        'reflected': True,
                        'response': reflected['response'],
                        'location': reflected['location']
                    })
            
            except:
                pass
        
        return results
    
    def _test_get(self, surface, token):
        """Test GET parameter reflection"""
        try:
            # Build URL with token
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            
            parsed = urlparse(surface['url'])
            params = parse_qs(parsed.query)
            params[surface['parameter']] = [token]
            
            new_query = urlencode(params, doseq=True)
            test_url = urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(test_url, headers=headers, timeout=10, verify=False)
            
            # Check if token is reflected
            if token in response.text:
                return {
                    'response': response.text,
                    'location': self._find_reflection_location(response.text, token)
                }
        
        except:
            pass
        
        return None
    
    def _test_post(self, surface, token):
        """Test POST parameter reflection"""
        try:
            data = {surface['parameter']: token}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.post(surface['url'], data=data, headers=headers, timeout=10, verify=False)
            
            # Check if token is reflected
            if token in response.text:
                return {
                    'response': response.text,
                    'location': self._find_reflection_location(response.text, token)
                }
        
        except:
            pass
        
        return None
    
    def _find_reflection_location(self, html, token):
        """Find where in the HTML the token is reflected"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check various locations
        locations = []
        
        # In script tags
        for script in soup.find_all('script'):
            if script.string and token in script.string:
                locations.append('script')
        
        # In attributes
        for tag in soup.find_all(True):
            for attr, value in tag.attrs.items():
                if isinstance(value, str) and token in value:
                    locations.append(f'attribute:{tag.name}:{attr}')
        
        # In text content
        if token in soup.get_text():
            locations.append('html_body')
        
        return locations if locations else ['unknown']
