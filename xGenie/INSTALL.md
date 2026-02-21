# xGenie Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip3
- nmap
- Chrome/Chromium (for dynamic XSS scanning)

## Debian/Ubuntu Installation

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip nmap chromium-browser
```

### 2. Build .deb Package

```bash
chmod +x build_deb.sh
./build_deb.sh
```

### 3. Install Package

```bash
sudo dpkg -i dist/xgenie_1.0.0_amd64.deb
```

### 4. Fix Dependencies (if needed)

```bash
sudo apt-get install -f
```

## Manual Installation

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install system dependencies
sudo apt install nmap
```

## Usage

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
# Start web server
xgenie server --port 5000

# Access at http://localhost:5000
```

## Troubleshooting

### Selenium/Chrome Issues

If dynamic XSS scanning fails:

```bash
# Install ChromeDriver
sudo apt install chromium-chromedriver
```

### Permission Issues

```bash
# Run nmap scans with sudo if needed
sudo xgenie scan example.com
```

## Legal Notice

This tool must only be used for:
- Authorized security assessments
- Systems you own or have explicit permission to test
- Educational purposes with proper authorization

Unauthorized use is illegal and unethical.
