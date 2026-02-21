import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class AdminFinder:
    def __init__(self, target):
        self.target = target
        if not target.startswith('http'):
            self.base_url = f'https://{target}'
        else:
            self.base_url = target
        
        # Common admin paths
        self.paths = [
            '/admin', '/admin/', '/administrator', '/administrator/',
            '/wp-admin', '/wp-admin/', '/wp-login.php',
            '/admin/login', '/admin/login.php', '/admin/index.php',
            '/login', '/login/', '/signin', '/signin/',
            '/user/login', '/auth/login', '/account/login',
            '/cpanel', '/cPanel', '/webmail',
            '/phpmyadmin', '/phpMyAdmin', '/pma',
            '/manager', '/manager/html',
            '/admin/dashboard', '/dashboard',
            '/console', '/admin-console',
            '/backend', '/backend/',
            '/cms', '/cms/',
            '/panel', '/control',
            '/admin.php', '/login.php', '/admin.html',
            '/adminer.php', '/adminer',
            '/admin/cp', '/admincp',
            '/modcp', '/moderator',
            '/webadmin', '/sysadmin',
            '/admin1', '/admin2', '/admin3',
            '/_admin', '/secret', '/hidden'
        ]
    
    def check_path(self, path):
        url = self.base_url + path
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5, verify=False, allow_redirects=False)
            
            status = response.status_code
            
            if status == 200:
                return {'path': path, 'url': url, 'status': 200, 'state': 'Found'}
            elif status == 401 or status == 403:
                return {'path': path, 'url': url, 'status': status, 'state': 'Forbidden/Auth Required'}
            elif status == 301 or status == 302:
                location = response.headers.get('Location', '')
                return {'path': path, 'url': url, 'status': status, 'state': f'Redirect to {location}'}
            
        except:
            pass
        
        return None
    
    def find(self):
        result = {
            'target': self.base_url,
            'found': [],
            'forbidden': [],
            'redirects': []
        }
        
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(self.check_path, path): path for path in self.paths}
                
                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        if res['state'] == 'Found':
                            result['found'].append(res)
                        elif 'Forbidden' in res['state'] or 'Auth' in res['state']:
                            result['forbidden'].append(res)
                        elif 'Redirect' in res['state']:
                            result['redirects'].append(res)
            
            if not result['found'] and not result['forbidden'] and not result['redirects']:
                return {'error': 'Unable to retrieve admin panel data'}
            
            return result
            
        except Exception as e:
            return {'error': f'Unable to retrieve data: {str(e)}'}
