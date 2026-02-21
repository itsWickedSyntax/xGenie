class RiskScorer:
    def __init__(self):
        self.weights = {
            'context': {
                'html_body': 8,
                'html_attribute': 7,
                'script_string': 9,
                'script_raw': 10,
                'event_handler': 9,
                'url_attribute': 6,
                'unknown': 5
            },
            'method': {
                'GET': 9,
                'POST': 7
            },
            'sink': {
                'innerHTML': 8,
                'outerHTML': 8,
                'document.write': 9,
                'eval': 10,
                'setTimeout': 9,
                'location': 7
            }
        }
    
    def calculate_risk(self, vulnerability):
        """
        Calculate weighted risk score for XSS vulnerability
        Score: 0-100
        """
        score = 0
        
        # Context weight
        context = vulnerability.get('context', 'unknown')
        score += self.weights['context'].get(context, 5) * 5
        
        # Method weight
        method = vulnerability.get('method', 'GET')
        score += self.weights['method'].get(method, 5) * 3
        
        # Sink weight (for DOM XSS)
        if 'sink' in vulnerability:
            sink = vulnerability['sink']
            sink_base = sink.split('(')[0].split('.')[0] if '(' in sink or '.' in sink else sink
            score += self.weights['sink'].get(sink_base, 5) * 4
        
        # Exploitability factors
        exploitability = 'High'
        
        if context in ['script_raw', 'eval', 'event_handler']:
            exploitability = 'Critical'
            score += 10
        elif context in ['script_string', 'html_body']:
            exploitability = 'High'
            score += 5
        elif context in ['html_attribute', 'url_attribute']:
            exploitability = 'Medium'
        else:
            exploitability = 'Low'
            score -= 5
        
        # Normalize score
        score = min(max(score, 0), 100)
        
        # Determine severity
        if score >= 80:
            severity = 'Critical'
        elif score >= 60:
            severity = 'High'
        elif score >= 40:
            severity = 'Medium'
        else:
            severity = 'Low'
        
        return {
            'score': score,
            'severity': severity,
            'exploitability': exploitability
        }
