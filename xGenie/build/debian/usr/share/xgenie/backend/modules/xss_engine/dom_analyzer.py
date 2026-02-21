import re
from bs4 import BeautifulSoup
import requests

class DOMAnalyzer:
    def __init__(self, base_url):
        self.base_url = base_url
        
        # Dangerous DOM sinks
        self.sinks = [
            'innerHTML',
            'outerHTML',
            'document.write',
            'document.writeln',
            'eval',
            'setTimeout',
            'setInterval',
            'Function',
            'execScript',
            'location',
            'location.href',
            'location.replace',
            'location.assign'
        ]
        
        # DOM sources (user-controllable)
        self.sources = [
            'location.hash',
            'location.search',
            'document.URL',
            'document.documentURI',
            'document.referrer',
            'window.name',
            'document.cookie'
        ]
    
    def analyze_dom_sinks(self, endpoints):
        """
        Analyze JavaScript code for DOM-based XSS vulnerabilities
        """
        vulnerabilities = []
        
        for endpoint in endpoints:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(endpoint['url'], headers=headers, timeout=10, verify=False)
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Analyze inline scripts
                for script in soup.find_all('script'):
                    if script.string:
                        vulns = self._analyze_script(script.string, endpoint['url'])
                        vulnerabilities.extend(vulns)
                
                # Analyze external scripts (basic)
                for script in soup.find_all('script', src=True):
                    src = script['src']
                    if src.startswith('/') or self.base_url in src:
                        # Only analyze same-origin scripts
                        try:
                            script_url = src if src.startswith('http') else self.base_url + src
                            script_response = requests.get(script_url, headers=headers, timeout=5, verify=False)
                            vulns = self._analyze_script(script_response.text, script_url)
                            vulnerabilities.extend(vulns)
                        except:
                            pass
            
            except:
                pass
        
        return vulnerabilities
    
    def _analyze_script(self, script_content, url):
        """Analyze JavaScript code for DOM XSS patterns"""
        vulnerabilities = []
        
        # Look for source -> sink data flow
        for source in self.sources:
            if source in script_content:
                for sink in self.sinks:
                    # Check if source data flows to sink
                    if self._check_data_flow(script_content, source, sink):
                        vulnerabilities.append({
                            'url': url,
                            'source': source,
                            'sink': sink,
                            'type': 'DOM-based XSS',
                            'code_snippet': self._extract_vulnerable_code(script_content, sink)
                        })
        
        return vulnerabilities
    
    def _check_data_flow(self, script, source, sink):
        """
        Check if data from source flows to sink
        This is a simplified static analysis
        """
        # Pattern: var x = location.hash; element.innerHTML = x;
        # Look for variable assignment from source
        source_pattern = rf'(\w+)\s*=\s*.*{re.escape(source)}'
        matches = re.findall(source_pattern, script)
        
        if matches:
            for var_name in matches:
                # Check if this variable is used in a sink
                sink_pattern = rf'{re.escape(sink)}\s*[=\(].*{re.escape(var_name)}'
                if re.search(sink_pattern, script):
                    return True
        
        # Direct flow: element.innerHTML = location.hash
        direct_pattern = rf'{re.escape(sink)}\s*[=\(].*{re.escape(source)}'
        if re.search(direct_pattern, script):
            return True
        
        return False
    
    def _extract_vulnerable_code(self, script, sink):
        """Extract the vulnerable code snippet"""
        lines = script.split('\n')
        
        for i, line in enumerate(lines):
            if sink in line:
                # Return context
                start = max(0, i-2)
                end = min(len(lines), i+3)
                return '\n'.join(lines[start:end])
        
        return ''
