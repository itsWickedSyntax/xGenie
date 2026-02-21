# xGenie Architecture

## Overview

xGenie is a production-ready security intelligence platform built with real data collection capabilities. NO mock data, NO simulations.

## Core Modules

### 1. WHOIS Intelligence (`backend/modules/whois_intel.py`)
- Real WHOIS lookups using python-whois
- Domain registration data
- Nameserver information
- Organization details

### 2. DNS Intelligence (`backend/modules/dns_intel.py`)
- Live DNS queries using dnspython
- A, AAAA, MX, NS, TXT, SOA records
- SPF, DMARC, DKIM detection
- Real-time resolution

### 3. Port Scanner (`backend/modules/port_scanner.py`)
- Real TCP scanning using python-nmap
- Service detection
- Banner grabbing
- Configurable scan depth

### 4. Technology Detector (`backend/modules/tech_detector.py`)
- HTTP header analysis
- HTML parsing with BeautifulSoup
- builtwith integration
- Framework/CMS detection

### 5. Security Analyzer (`backend/modules/security_analyzer.py`)
- Security header validation
- TLS/SSL configuration analysis
- Cookie security checks
- Vulnerability detection

### 6. Admin Panel Finder (`backend/modules/admin_finder.py`)
- Common path enumeration
- HTTP status code analysis
- Concurrent scanning
- Framework-specific routes

## Advanced XSS Detection Engine

### Architecture

```
backend/modules/xss_engine/
├── crawler.py              # Dynamic web crawler
├── parameter_mapper.py     # Attack surface mapping
├── reflection_tester.py    # Harmless token injection
├── context_classifier.py   # Context analysis
├── dom_analyzer.py         # DOM sink detection
├── risk_scorer.py          # Weighted risk scoring
└── xss_scanner.py          # Main orchestrator
```

### Detection Pipeline

1. **Dynamic Crawling** (`crawler.py`)
   - Static HTML parsing
   - JavaScript-rendered content (Selenium)
   - Form discovery
   - AJAX endpoint detection

2. **Parameter Mapping** (`parameter_mapper.py`)
   - URL parameters
   - Form inputs
   - Attack surface enumeration

3. **Reflection Testing** (`reflection_tester.py`)
   - Harmless unique token generation
   - GET/POST parameter injection
   - Reflection location detection

4. **Context Classification** (`context_classifier.py`)
   - HTML body context
   - HTML attribute context
   - JavaScript string context
   - Script raw context
   - Event handler context
   - URL attribute context

5. **DOM Analysis** (`dom_analyzer.py`)
   - Dangerous sink detection:
     - innerHTML, outerHTML
     - document.write
     - eval, setTimeout, setInterval
     - location manipulation
   - Source tracking:
     - location.hash, location.search
     - document.URL, document.referrer
     - window.name
   - Data flow analysis

6. **Risk Scoring** (`risk_scorer.py`)
   - Weighted scoring algorithm
   - Context-based risk calculation
   - Exploitability assessment
   - Severity classification

## Web Interface

### Frontend (`frontend/`)
- Modern responsive design
- Real-time scan progress
- Color scheme: #1B1B1C (bg), #333333 (layers), #0FE9FF (accent)
- Results visualization
- JSON export

### Backend API (`backend/server.py`)
- Flask REST API
- Asynchronous scanning
- Status polling
- Result retrieval

## Data Flow

```
User Input → Scanner → Modules → Real Network Requests → Data Collection → Analysis → Results
```

## Key Principles

1. **Real Data Only**: All data comes from actual network activity
2. **No Mocking**: No simulated or fabricated results
3. **Error Handling**: Returns "Unable to retrieve data" on failure
4. **Production Ready**: Installable .deb package
5. **Authorized Use**: Built for defensive security operations

## Dependencies

- requests: HTTP client
- dnspython: DNS queries
- python-whois: WHOIS lookups
- python-nmap: Port scanning
- beautifulsoup4: HTML parsing
- selenium: Dynamic content
- flask: Web framework
- cryptography/pyOpenSSL: TLS analysis

## Deployment

- Debian package (.deb)
- CLI interface
- Web server mode
- Systemd service ready
