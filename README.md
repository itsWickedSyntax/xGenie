# xGenie - Security Intelligence Platform


**Production-ready website and infrastructure reconnaissance platform for authorized defensive security operations.**

⚠️ **AUTHORIZED USE ONLY** - See [LEGAL_NOTICE.txt](LEGAL_NOTICE.txt)

---

## 🎯 Overview

xGenie is a comprehensive security intelligence platform that performs real-world reconnaissance and vulnerability assessment. This is NOT a demo or simulation - all data is obtained from actual network activity.

### Key Principles

- ✅ **Real Data Only** - No mock data, no simulations
- ✅ **Production Ready** - Installable .deb package
- ✅ **Comprehensive** - 6 core modules + advanced XSS engine
- ✅ **Ethical** - Built for authorized defensive operations only

---

## 🚀 Features

### Core Intelligence Modules

1. **WHOIS & Ownership Intelligence**
   - Domain registration data, nameservers, organization details
   - Real-time WHOIS lookups

2. **Port Scanning & Service Discovery**
   - TCP port scanning with nmap integration
   - Service detection and banner grabbing

3. **Technology Stack Detection**
   - Web servers, frameworks, CMS, JavaScript libraries
   - CDN and hosting provider identification

4. **DNS Intelligence**
   - A, AAAA, MX, NS, TXT, SOA records
   - SPF, DMARC, DKIM analysis

5. **Admin Panel Discovery**
   - Common path enumeration
   - Framework-specific routes

6. **Security Analysis**
   - Missing security headers
   - TLS/SSL configuration
   - Cookie security
   - Risk scoring

### Advanced XSS Detection Engine

- **Dynamic Crawler** - Static + JavaScript-rendered content
- **Reflection Testing** - Harmless token-based detection
- **Context Classification** - HTML, attribute, script contexts
- **DOM Sink Analysis** - innerHTML, eval, setTimeout, location
- **Risk Scoring** - Weighted vulnerability assessment

See [FEATURES.md](FEATURES.md) for complete feature list.

---

## 📦 Installation

### Quick Install (Debian/Ubuntu)

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip nmap chromium-browser

# Build package
chmod +x build_deb.sh
./build_deb.sh

# Install
sudo dpkg -i dist/xgenie_1.0.0_amd64.deb
```

### Manual Install

```bash
pip3 install -r requirements.txt
sudo apt install nmap
```

See [INSTALL.md](INSTALL.md) for detailed instructions.

---

## 💻 Usage

### CLI Mode

```bash
# Basic scan
xgenie scan example.com

# Full scan with XSS detection
xgenie scan example.com --full

# Save results
xgenie scan example.com --output results.json
```

### Web Interface

```bash
# Start server
xgenie server --port 5000

# Open browser to http://localhost:5000
```

See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more examples.

---

## 🏗️ Architecture

```
xGenie/
├── backend/
│   ├── core/
│   │   ├── scanner.py          # Main orchestrator
│   │   └── reporter.py         # Results formatting
│   ├── modules/
│   │   ├── whois_intel.py      # WHOIS lookups
│   │   ├── dns_intel.py        # DNS enumeration
│   │   ├── port_scanner.py     # Port scanning
│   │   ├── tech_detector.py    # Technology detection
│   │   ├── admin_finder.py     # Admin panel discovery
│   │   ├── security_analyzer.py # Security analysis
│   │   └── xss_engine/         # XSS detection
│   │       ├── crawler.py      # Dynamic crawler
│   │       ├── parameter_mapper.py
│   │       ├── reflection_tester.py
│   │       ├── context_classifier.py
│   │       ├── dom_analyzer.py
│   │       └── risk_scorer.py
│   ├── server.py               # Flask API
│   └── cli.py                  # CLI interface
├── frontend/
│   ├── templates/
│   │   └── index.html          # Web UI
│   └── static/
│       ├── css/style.css       # Styling
│       └── js/app.js           # Frontend logic
└── build_deb.sh                # Package builder
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture.

---

## 🎨 User Interface

### Modern Dark Theme
- Background: `#1B1B1C`
- Layers: `#333333`
- Accent: `#0FE9FF`

### Features
- Real-time scan progress
- Interactive results dashboard
- Color-coded severity indicators
- JSON export functionality

---

## 📊 Example Output

```
[WHOIS INTELLIGENCE]
  Registrar: GoDaddy.com, LLC
  Organization: Example Corp
  Country: US

[DNS RECORDS]
  A Records: 93.184.216.34
  MX Records: 10 mail.example.com

[OPEN PORTS]
  Port  Service  Banner
  22    ssh      OpenSSH 8.2p1
  80    http     nginx/1.18.0
  443   https    nginx/1.18.0

[SECURITY ANALYSIS]
  Risk Score: 45/100
  Missing Headers: Strict-Transport-Security, CSP
  Vulnerabilities: 5 found

[XSS DETECTION]
  Endpoints Tested: 15
  Vulnerabilities: 2 found (1 Reflected, 1 DOM-based)
```

---

## ⚖️ Legal & Ethics

### Authorized Use Only

This tool is intended ONLY for:
- ✅ Authorized security assessments
- ✅ Systems you own or have explicit permission to test
- ✅ Defensive security operations
- ✅ Educational purposes with proper authorization

### Prohibited Uses

- ❌ Scanning systems without authorization
- ❌ Unauthorized access attempts
- ❌ Malicious reconnaissance
- ❌ Any illegal activity

**Unauthorized use is illegal and may result in criminal prosecution.**

See [LEGAL_NOTICE.txt](LEGAL_NOTICE.txt) for complete legal information.

---

## 🛠️ Technical Details

### Dependencies
- Python 3.8+
- Flask, requests, dnspython
- python-whois, python-nmap
- BeautifulSoup4, Selenium
- cryptography, pyOpenSSL

### Compatibility
- Debian/Ubuntu Linux
- Python 3.8 or higher
- Chrome/Chromium (for XSS scanning)

---

## 📝 Documentation

- [FEATURES.md](FEATURES.md) - Complete feature list
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [INSTALL.md](INSTALL.md) - Installation guide
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Usage examples
- [LEGAL_NOTICE.txt](LEGAL_NOTICE.txt) - Legal information

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

**Legal Notice**: This software is for authorized use only. Users are responsible for compliance with all applicable laws.

---

## 🤝 Contributing

This is a security tool. Contributions should:
- Maintain real data collection (no mocking)
- Follow ethical security practices
- Include proper error handling
- Document authorization requirements

---

## ⚠️ Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. Users are solely responsible for their actions. The developers assume no liability for misuse.

---

**xGenie v1.0.0** | Built for authorized security professionals
