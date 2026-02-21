import requests
import ssl
import socket
from urllib.parse import urlparse
from OpenSSL import SSL, crypto

class SecurityAnalyzer:
    def __init__(self, target):
        self.target = target
        if not target.startswith('http'):
            self.url = f'https://{target}'
        else:
            self.url = target
        
        self.parsed = urlparse(self.url)
        self.hostname = self.parsed.hostname
    
    def analyze(self):
        result = {
            'url': self.url,
            'missing_headers': [],
            'present_headers': {},
            'tls_info': {},
            'vulnerabilities': [],
            'cookies': [],
            'risk_score': 0
        }
        
        try:
            # HTTP Headers Analysis
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10, verify=False, allow_redirects=True)
            
            # Check security headers
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME Sniffing Protection',
                'Content-Security-Policy': 'CSP',
                'X-XSS-Protection': 'XSS Protection',
                'Referrer-Policy': 'Referrer Policy',
                'Permissions-Policy': 'Permissions Policy'
            }
            
            for header, desc in security_headers.items():
                if header in response.headers:
                    result['present_headers'][header] = response.headers[header]
                else:
                    result['missing_headers'].append(header)
                    result['vulnerabilities'].append({
                        'type': 'Missing Security Header',
                        'header': header,
                        'description': f'Missing {desc}',
                        'severity': 'Medium'
                    })
            
            # Check for X-Powered-By disclosure
            if 'X-Powered-By' in response.headers:
                result['vulnerabilities'].append({
                    'type': 'Information Disclosure',
                    'header': 'X-Powered-By',
                    'value': response.headers['X-Powered-By'],
                    'severity': 'Low'
                })
            
            # Check for Server header disclosure
            if 'Server' in response.headers:
                server = response.headers['Server']
                if any(ver in server for ver in ['/', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']):
                    result['vulnerabilities'].append({
                        'type': 'Information Disclosure',
                        'header': 'Server',
                        'value': server,
                        'severity': 'Low'
                    })
            
            # Cookie analysis
            if 'Set-Cookie' in response.headers:
                cookies = response.headers['Set-Cookie']
                if 'secure' not in cookies.lower():
                    result['vulnerabilities'].append({
                        'type': 'Insecure Cookie',
                        'description': 'Cookie missing Secure flag',
                        'severity': 'Medium'
                    })
                if 'httponly' not in cookies.lower():
                    result['vulnerabilities'].append({
                        'type': 'Insecure Cookie',
                        'description': 'Cookie missing HttpOnly flag',
                        'severity': 'Medium'
                    })
            
            # TLS/SSL Analysis
            if self.url.startswith('https'):
                try:
                    context = ssl.create_default_context()
                    with socket.create_connection((self.hostname, 443), timeout=5) as sock:
                        with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                            cert = ssock.getpeercert()
                            cipher = ssock.cipher()
                            
                            result['tls_info'] = {
                                'version': ssock.version(),
                                'cipher': cipher[0] if cipher else None,
                                'bits': cipher[2] if cipher else None,
                                'issuer': dict(x[0] for x in cert.get('issuer', [])),
                                'subject': dict(x[0] for x in cert.get('subject', [])),
                                'notAfter': cert.get('notAfter'),
                                'notBefore': cert.get('notBefore')
                            }
                            
                            # Check for weak ciphers
                            if cipher and cipher[0]:
                                cipher_name = cipher[0].lower()
                                if any(weak in cipher_name for weak in ['rc4', 'des', 'md5', 'null']):
                                    result['vulnerabilities'].append({
                                        'type': 'Weak Cipher',
                                        'cipher': cipher[0],
                                        'severity': 'High'
                                    })
                            
                            # Check TLS version
                            if ssock.version() in ['TLSv1', 'TLSv1.1', 'SSLv2', 'SSLv3']:
                                result['vulnerabilities'].append({
                                    'type': 'Outdated TLS Version',
                                    'version': ssock.version(),
                                    'severity': 'High'
                                })
                except:
                    pass
            
            # Calculate risk score
            risk_score = 0
            for vuln in result['vulnerabilities']:
                if vuln['severity'] == 'High':
                    risk_score += 10
                elif vuln['severity'] == 'Medium':
                    risk_score += 5
                elif vuln['severity'] == 'Low':
                    risk_score += 2
            
            result['risk_score'] = min(risk_score, 100)
            
            if not result['vulnerabilities'] and not result['missing_headers']:
                return {'error': 'Unable to retrieve security data'}
            
            return result
            
        except Exception as e:
            return {'error': f'Unable to retrieve data: {str(e)}'}
