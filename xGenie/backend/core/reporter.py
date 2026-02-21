import json
from colorama import Fore, Style
from tabulate import tabulate

class Reporter:
    def __init__(self, results):
        self.results = results
    
    def print_console(self):
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}SCAN RESULTS: {self.results['target']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        # WHOIS
        if self.results.get('whois') and 'error' not in self.results['whois']:
            print(f"{Fore.YELLOW}[WHOIS INTELLIGENCE]{Style.RESET_ALL}")
            whois = self.results['whois']
            if whois.get('registrar'):
                print(f"  Registrar: {whois['registrar']}")
            if whois.get('organization'):
                print(f"  Organization: {whois['organization']}")
            if whois.get('country'):
                print(f"  Country: {whois['country']}")
            print()
        
        # DNS
        if self.results.get('dns') and 'error' not in self.results['dns']:
            print(f"{Fore.YELLOW}[DNS RECORDS]{Style.RESET_ALL}")
            dns = self.results['dns']
            if dns.get('A'):
                print(f"  A Records: {', '.join(dns['A'])}")
            if dns.get('MX'):
                print(f"  MX Records: {', '.join(dns['MX'])}")
            print()
        
        # Ports
        if self.results.get('ports') and 'error' not in self.results['ports']:
            print(f"{Fore.YELLOW}[OPEN PORTS]{Style.RESET_ALL}")
            ports = self.results['ports'].get('open_ports', [])
            if ports:
                table = [[p['port'], p['service'], p.get('banner', 'N/A')] for p in ports]
                print(tabulate(table, headers=['Port', 'Service', 'Banner'], tablefmt='simple'))
            else:
                print("  No open ports detected")
            print()
        
        # Technology
        if self.results.get('tech_stack') and 'error' not in self.results['tech_stack']:
            print(f"{Fore.YELLOW}[TECHNOLOGY STACK]{Style.RESET_ALL}")
            tech = self.results['tech_stack']
            if tech.get('web_server'):
                print(f"  Web Server: {tech['web_server']}")
            if tech.get('frameworks'):
                print(f"  Frameworks: {', '.join(tech['frameworks'])}")
            if tech.get('cms'):
                print(f"  CMS: {tech['cms']}")
            print()
        
        # Security
        if self.results.get('security') and 'error' not in self.results['security']:
            print(f"{Fore.YELLOW}[SECURITY ANALYSIS]{Style.RESET_ALL}")
            sec = self.results['security']
            if sec.get('missing_headers'):
                print(f"  {Fore.RED}Missing Headers: {', '.join(sec['missing_headers'])}{Style.RESET_ALL}")
            if sec.get('vulnerabilities'):
                print(f"  {Fore.RED}Vulnerabilities: {len(sec['vulnerabilities'])} found{Style.RESET_ALL}")
            print()
        
        # XSS
        if self.results.get('xss') and 'error' not in self.results['xss']:
            print(f"{Fore.YELLOW}[XSS DETECTION]{Style.RESET_ALL}")
            xss = self.results['xss']
            if xss.get('vulnerabilities'):
                print(f"  {Fore.RED}XSS Issues: {len(xss['vulnerabilities'])} found{Style.RESET_ALL}")
                for vuln in xss['vulnerabilities'][:5]:
                    print(f"    - {vuln['url']} ({vuln['type']})")
            else:
                print(f"  {Fore.GREEN}No XSS vulnerabilities detected{Style.RESET_ALL}")
            print()
    
    def save_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
