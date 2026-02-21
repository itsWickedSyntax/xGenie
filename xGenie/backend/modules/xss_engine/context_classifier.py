import re
from bs4 import BeautifulSoup

class ContextClassifier:
    def __init__(self):
        self.contexts = []
    
    def classify_contexts(self, reflections):
        """
        Classify the context where user input is reflected:
        - HTML body
        - HTML attribute
        - JavaScript context
        - Script tag
        - Event handler
        """
        classified = []
        
        for reflection in reflections:
            context = self._determine_context(reflection['response'], reflection['token'])
            
            # Generate appropriate payload based on context
            payload = self._generate_payload(context)
            
            classified.append({
                'url': reflection['url'],
                'method': reflection['method'],
                'parameter': reflection['parameter'],
                'token': reflection['token'],
                'reflected': True,
                'context': context,
                'payload': payload,
                'evidence': self._extract_evidence(reflection['response'], reflection['token'])
            })
        
        return classified
    
    def _determine_context(self, html, token):
        """Determine the context where token appears"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check if in script tag
        for script in soup.find_all('script'):
            if script.string and token in script.string:
                # Check if in string or raw JS
                script_content = script.string
                token_pos = script_content.find(token)
                
                # Look around the token
                before = script_content[max(0, token_pos-10):token_pos]
                after = script_content[token_pos+len(token):token_pos+len(token)+10]
                
                if '"' in before or "'" in before:
                    return 'script_string'
                else:
                    return 'script_raw'
        
        # Check if in attribute
        for tag in soup.find_all(True):
            for attr, value in tag.attrs.items():
                if isinstance(value, str) and token in value:
                    # Event handler attributes
                    if attr.startswith('on'):
                        return 'event_handler'
                    # href/src attributes
                    elif attr in ['href', 'src', 'action', 'data']:
                        return 'url_attribute'
                    else:
                        return 'html_attribute'
        
        # Check if in HTML body
        if token in soup.get_text():
            return 'html_body'
        
        return 'unknown'
    
    def _generate_payload(self, context):
        """Generate context-appropriate XSS payload"""
        payloads = {
            'html_body': '<script>alert(1)</script>',
            'html_attribute': '" onload="alert(1)" x="',
            'script_string': '"; alert(1); //',
            'script_raw': '; alert(1); //',
            'event_handler': 'alert(1)',
            'url_attribute': 'javascript:alert(1)',
            'unknown': '<script>alert(1)</script>'
        }
        
        return payloads.get(context, '<script>alert(1)</script>')
    
    def _extract_evidence(self, html, token):
        """Extract code snippet showing the reflection"""
        # Find the line containing the token
        lines = html.split('\n')
        for i, line in enumerate(lines):
            if token in line:
                # Return context around the reflection
                start = max(0, i-2)
                end = min(len(lines), i+3)
                return '\n'.join(lines[start:end])
        
        return ''
