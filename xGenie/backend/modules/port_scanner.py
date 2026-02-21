import socket
import nmap
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
    
    def scan(self, deep=False):
        result = {
            'target': self.target,
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': []
        }
        
        try:
            # Resolve target to IP
            ip = socket.gethostbyname(self.target)
            result['ip'] = ip
            
            # Use nmap for real scanning
            nm = nmap.PortScanner()
            
            if deep:
                # Full scan (slower)
                ports = '1-1000'
            else:
                # Common ports only
                ports = ','.join(map(str, self.common_ports))
            
            # Perform scan
            nm.scan(ip, ports, arguments='-sV -T4')
            
            if ip in nm.all_hosts():
                for proto in nm[ip].all_protocols():
                    ports_data = nm[ip][proto]
                    
                    for port in ports_data:
                        port_info = ports_data[port]
                        state = port_info['state']
                        
                        port_data = {
                            'port': port,
                            'protocol': proto,
                            'state': state,
                            'service': port_info.get('name', 'unknown'),
                            'product': port_info.get('product', ''),
                            'version': port_info.get('version', ''),
                            'banner': f"{port_info.get('product', '')} {port_info.get('version', '')}".strip()
                        }
                        
                        if state == 'open':
                            result['open_ports'].append(port_data)
                        elif state == 'closed':
                            result['closed_ports'].append(port_data)
                        elif state == 'filtered':
                            result['filtered_ports'].append(port_data)
            
            if not result['open_ports'] and not result['closed_ports']:
                return {'error': 'Unable to retrieve port data'}
            
            return result
            
        except Exception as e:
            return {'error': f'Unable to retrieve data: {str(e)}'}
