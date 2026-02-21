import socket
import validators
from colorama import Fore, Style
from backend.modules.whois_intel import WhoisIntel
from backend.modules.port_scanner import PortScanner
from backend.modules.tech_detector import TechDetector
from backend.modules.dns_intel import DNSIntel
from backend.modules.admin_finder import AdminFinder
from backend.modules.security_analyzer import SecurityAnalyzer
from backend.modules.xss_engine.xss_scanner import XSSScanner

class Scanner:
    def __init__(self, target):
        self.target = target.strip()
        self.results = {
            'target': self.target,
            'status': 'initialized',
            'whois': None,
            'ports': None,
            'tech_stack': None,
            'dns': None,
            'admin_panels': None,
            'security': None,
            'xss': None
        }
    
    def run_full_scan(self, deep=False):
        print(f"{Fore.CYAN}[*] Starting reconnaissance...{Style.RESET_ALL}")
        
        # WHOIS Intelligence
        print(f"{Fore.CYAN}[*] Gathering WHOIS intelligence...{Style.RESET_ALL}")
        try:
            whois_intel = WhoisIntel(self.target)
            self.results['whois'] = whois_intel.gather()
        except Exception as e:
            print(f"{Fore.RED}[!] WHOIS error: {e}{Style.RESET_ALL}")
            self.results['whois'] = {'error': str(e)}
        
        # DNS Intelligence
        print(f"{Fore.CYAN}[*] DNS enumeration...{Style.RESET_ALL}")
        try:
            dns_intel = DNSIntel(self.target)
            self.results['dns'] = dns_intel.gather()
        except Exception as e:
            print(f"{Fore.RED}[!] DNS error: {e}{Style.RESET_ALL}")
            self.results['dns'] = {'error': str(e)}
        
        # Port Scanning
        print(f"{Fore.CYAN}[*] Port scanning...{Style.RESET_ALL}")
        try:
            port_scanner = PortScanner(self.target)
            self.results['ports'] = port_scanner.scan(deep=deep)
        except Exception as e:
            print(f"{Fore.RED}[!] Port scan error: {e}{Style.RESET_ALL}")
            self.results['ports'] = {'error': str(e)}
        
        # Technology Detection
        print(f"{Fore.CYAN}[*] Detecting technology stack...{Style.RESET_ALL}")
        try:
            tech_detector = TechDetector(self.target)
            self.results['tech_stack'] = tech_detector.detect()
        except Exception as e:
            print(f"{Fore.RED}[!] Tech detection error: {e}{Style.RESET_ALL}")
            self.results['tech_stack'] = {'error': str(e)}
        
        # Admin Panel Discovery
        print(f"{Fore.CYAN}[*] Discovering admin panels...{Style.RESET_ALL}")
        try:
            admin_finder = AdminFinder(self.target)
            self.results['admin_panels'] = admin_finder.find()
        except Exception as e:
            print(f"{Fore.RED}[!] Admin finder error: {e}{Style.RESET_ALL}")
            self.results['admin_panels'] = {'error': str(e)}
        
        # Security Analysis
        print(f"{Fore.CYAN}[*] Analyzing security posture...{Style.RESET_ALL}")
        try:
            security_analyzer = SecurityAnalyzer(self.target)
            self.results['security'] = security_analyzer.analyze()
        except Exception as e:
            print(f"{Fore.RED}[!] Security analysis error: {e}{Style.RESET_ALL}")
            self.results['security'] = {'error': str(e)}
        
        # XSS Detection
        if deep:
            print(f"{Fore.CYAN}[*] Running XSS detection engine...{Style.RESET_ALL}")
            try:
                xss_scanner = XSSScanner(self.target)
                self.results['xss'] = xss_scanner.scan()
            except Exception as e:
                print(f"{Fore.RED}[!] XSS scan error: {e}{Style.RESET_ALL}")
                self.results['xss'] = {'error': str(e)}
        
        self.results['status'] = 'completed'
        return self.results
