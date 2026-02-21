# xGenie Quick Reference Card

## Installation

```bash
# One-line install
sudo apt install -y python3 python3-pip nmap && ./build_deb.sh && sudo dpkg -i dist/xgenie_1.0.0_amd64.deb
```

## Basic Commands

```bash
# Basic scan
xgenie scan example.com

# Full scan with XSS
xgenie scan example.com --full

# Save results
xgenie scan example.com -o results.json

# Web interface
xgenie server --port 5000
```

## Module Overview

| Module | Function | Output |
|--------|----------|--------|
| WHOIS | Domain ownership | Registrar, dates, org |
| DNS | DNS records | A, MX, NS, TXT, SPF |
| Ports | Open ports | Port, service, banner |
| Tech | Technology stack | Server, CMS, frameworks |
| Admin | Admin panels | Found paths, status |
| Security | Security posture | Headers, TLS, risk score |
| XSS | XSS vulnerabilities | Reflected, DOM-based |

## XSS Engine Pipeline

```
1. Crawler → Discover endpoints
2. Mapper → Extract parameters
3. Tester → Inject tokens
4. Classifier → Analyze context
5. DOM Analyzer → Check sinks
6. Scorer → Calculate risk
```

## Risk Scores

| Score | Severity | Action |
|-------|----------|--------|
| 80-100 | Critical | Immediate fix |
| 60-79 | High | Fix soon |
| 40-59 | Medium | Schedule fix |
| 0-39 | Low | Monitor |

## Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied | Run with sudo |
| WHOIS timeout | Wait and retry |
| Port scan fails | Check nmap install |
| XSS scan fails | Install chromium-chromedriver |

## File Locations

```
/usr/local/bin/xgenie          # Main executable
/usr/share/xgenie/             # Application files
~/.xgenie/                     # User data (future)
```

## Output Format

```json
{
  "target": "example.com",
  "whois": {...},
  "dns": {...},
  "ports": {...},
  "tech_stack": {...},
  "security": {...},
  "xss": {...}
}
```

## Legal Checklist

- [ ] Written authorization obtained
- [ ] Scope documented
- [ ] Testing window agreed
- [ ] Contact information exchanged
- [ ] Findings will be reported responsibly

## Safe Test Targets

✅ example.com
✅ scanme.nmap.org
✅ testphp.vulnweb.com
✅ Your own domains

❌ Any unauthorized systems

## Support

- Documentation: See README.md
- Architecture: See ARCHITECTURE.md
- Examples: See USAGE_EXAMPLES.md
- Testing: See TEST_GUIDE.md
- Legal: See LEGAL_NOTICE.txt

## Quick Troubleshooting

```bash
# Verify installation
./verify_installation.sh

# Check dependencies
pip3 list | grep -E "flask|requests|dnspython|whois|nmap"

# Test basic functionality
xgenie scan example.com --output test.json && cat test.json

# Check logs (if installed as service)
journalctl -u xgenie
```

## Performance Tips

- Use basic scan for quick overview
- Use --full only when needed
- Scan during off-peak hours
- Respect rate limits
- Monitor resource usage

## Color Scheme

- Background: `#1B1B1C`
- Layers: `#333333`
- Accent: `#0FE9FF`
- Success: `#00FF00`
- Warning: `#FFA500`
- Error: `#FF6B6B`

## Version Info

- Version: 1.0.0
- Platform: Debian/Ubuntu Linux
- Python: 3.8+
- License: MIT (with legal notice)

---

**Remember: Authorized Use Only**

This tool is for defensive security operations only. Always obtain proper authorization before scanning any systems.
