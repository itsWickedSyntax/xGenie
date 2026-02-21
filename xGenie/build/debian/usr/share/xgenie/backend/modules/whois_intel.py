import whois
import socket
from datetime import datetime

class WhoisIntel:
    def __init__(self, target):
        self.target = target
    
    def gather(self):
        try:
            # Perform real WHOIS lookup
            w = whois.whois(self.target)
            
            result = {
                'domain': self.target,
                'registrar': w.registrar if hasattr(w, 'registrar') else None,
                'creation_date': str(w.creation_date) if hasattr(w, 'creation_date') else None,
                'expiration_date': str(w.expiration_date) if hasattr(w, 'expiration_date') else None,
                'updated_date': str(w.updated_date) if hasattr(w, 'updated_date') else None,
                'nameservers': w.name_servers if hasattr(w, 'name_servers') else [],
                'organization': w.org if hasattr(w, 'org') else None,
                'country': w.country if hasattr(w, 'country') else None,
                'state': w.state if hasattr(w, 'state') else None,
                'city': w.city if hasattr(w, 'city') else None,
                'emails': w.emails if hasattr(w, 'emails') else [],
                'status': w.status if hasattr(w, 'status') else None,
            }
            
            # Get IP and ASN info
            try:
                ip = socket.gethostbyname(self.target)
                result['ip_address'] = ip
            except:
                result['ip_address'] = None
            
            # Clean up None values
            result = {k: v for k, v in result.items() if v is not None}
            
            if not result or len(result) <= 1:
                return {'error': 'Unable to retrieve WHOIS data'}
            
            return result
            
        except Exception as e:
            return {'error': f'Unable to retrieve data: {str(e)}'}
