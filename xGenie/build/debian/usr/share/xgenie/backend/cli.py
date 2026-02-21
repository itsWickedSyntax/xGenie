#!/usr/bin/env python3
import sys
import argparse
from colorama import init, Fore, Style
from backend.core.scanner import Scanner
from backend.core.reporter import Reporter

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}
 ╔═╗ ╔═╗┌─┐┌┐┌┬┌─┐
 ╔╩╦╝ ║ ╦├┤ │││││├┤ 
 ╚═╝  ╚═╝└─┘┘└┘┴└─┘
{Style.RESET_ALL}
 Security Intelligence Platform v1.0.0
 {Fore.YELLOW}[!] Authorized Use Only{Style.RESET_ALL}
"""
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='xGenie Security Intelligence Platform')
    parser.add_argument('command', choices=['scan', 'server'], help='Command to execute')
    parser.add_argument('target', nargs='?', help='Target domain or IP')
    parser.add_argument('--port', type=int, default=5000, help='Server port (default: 5000)')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--full', action='store_true', help='Full scan (slower)')
    
    args = parser.parse_args()
    
    if args.command == 'server':
        from backend.server import app
        print(f"{Fore.GREEN}[+] Starting web server on http://localhost:{args.port}{Style.RESET_ALL}")
        app.run(host='0.0.0.0', port=args.port, debug=False)
    
    elif args.command == 'scan':
        if not args.target:
            print(f"{Fore.RED}[!] Target required for scan command{Style.RESET_ALL}")
            sys.exit(1)
        
        print(f"{Fore.GREEN}[+] Scanning target: {args.target}{Style.RESET_ALL}\n")
        
        scanner = Scanner(args.target)
        results = scanner.run_full_scan(deep=args.full)
        
        reporter = Reporter(results)
        reporter.print_console()
        
        if args.output:
            reporter.save_json(args.output)
            print(f"\n{Fore.GREEN}[+] Results saved to: {args.output}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
