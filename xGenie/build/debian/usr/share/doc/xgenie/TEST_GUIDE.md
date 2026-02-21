# xGenie Testing Guide

## Testing the Installation

### 1. Verify Installation

```bash
# Check if xgenie is installed
which xgenie

# Check version
xgenie --help
```

### 2. Test Basic Functionality

```bash
# Test with a safe, public domain (example.com is safe for testing)
xgenie scan example.com --output test_scan.json
```

### 3. Test Web Interface

```bash
# Start server
xgenie server --port 5000

# Open browser to http://localhost:5000
# Enter "example.com" as target
# Click "Start Reconnaissance"
```

## Safe Testing Targets

### Recommended Test Domains

These domains are safe for testing reconnaissance tools:

1. **example.com** - IANA reserved domain for testing
2. **scanme.nmap.org** - Intentionally vulnerable for testing
3. **testphp.vulnweb.com** - Test site for security tools
4. **Your own domains** - Always best to test on systems you own

### DO NOT Test On

- ❌ Government websites
- ❌ Financial institutions
- ❌ Healthcare systems
- ❌ Any site without authorization
- ❌ Production systems you don't own

## Module Testing

### Test WHOIS Module

```bash
# Should return registrar, dates, nameservers
xgenie scan example.com
# Check WHOIS section in output
```

### Test DNS Module

```bash
# Should return A, MX, NS records
xgenie scan example.com
# Check DNS section in output
```

### Test Port Scanner

```bash
# Should detect open ports (80, 443 typically)
xgenie scan example.com
# Check Ports section in output
```

### Test Technology Detection

```bash
# Should detect web server, frameworks
xgenie scan example.com
# Check Technology Stack section
```

### Test Security Analysis

```bash
# Should analyze headers, TLS
xgenie scan example.com
# Check Security Analysis section
```

### Test XSS Engine (Deep Scan)

```bash
# Full scan with XSS detection
xgenie scan testphp.vulnweb.com --full
# Check XSS Detection section
```

## Expected Results

### Example.com Expected Output

```
[WHOIS INTELLIGENCE]
  Registrar: IANA
  Organization: Internet Assigned Numbers Authority
  Country: US

[DNS RECORDS]
  A Records: 93.184.216.34
  MX Records: 0 .

[OPEN PORTS]
  Port  Service  Banner
  80    http     N/A
  443   https    N/A

[TECHNOLOGY STACK]
  Web Server: nginx or similar
  
[SECURITY ANALYSIS]
  Risk Score: Variable
  Missing Headers: Several expected
```

## Troubleshooting

### Issue: "Unable to retrieve WHOIS data"

**Cause**: WHOIS server timeout or rate limiting

**Solution**: 
- Wait a few minutes and retry
- Check internet connection
- Try a different domain

### Issue: "Unable to retrieve port data"

**Cause**: Firewall blocking, insufficient permissions

**Solution**:
- Run with sudo: `sudo xgenie scan example.com`
- Check if nmap is installed: `which nmap`
- Verify target is reachable: `ping example.com`

### Issue: XSS scan fails

**Cause**: Selenium/ChromeDriver not installed

**Solution**:
```bash
sudo apt install chromium-chromedriver
```

### Issue: "Permission denied"

**Cause**: Insufficient permissions for network scanning

**Solution**:
```bash
# Run with sudo for port scanning
sudo xgenie scan example.com
```

## Performance Testing

### Scan Duration Expectations

- **Basic Scan**: 30-60 seconds
- **Full Scan (with XSS)**: 2-5 minutes
- **Deep XSS Scan**: 5-15 minutes (depending on site size)

### Resource Usage

- **CPU**: Moderate (10-30% on modern systems)
- **Memory**: 100-500 MB
- **Network**: Depends on scan depth

## Validation Checklist

- [ ] Installation completes without errors
- [ ] CLI command executes successfully
- [ ] Web interface loads properly
- [ ] WHOIS data retrieves correctly
- [ ] DNS records resolve
- [ ] Port scanning works
- [ ] Technology detection functions
- [ ] Security analysis completes
- [ ] XSS engine runs (deep scan)
- [ ] JSON export works
- [ ] Results display correctly

## Automated Testing Script

```bash
#!/bin/bash
# test_xgenie.sh

echo "Testing xGenie Installation..."

# Test 1: Command exists
if command -v xgenie &> /dev/null; then
    echo "✓ xgenie command found"
else
    echo "✗ xgenie command not found"
    exit 1
fi

# Test 2: Basic scan
echo "Running basic scan on example.com..."
xgenie scan example.com --output test_output.json

if [ -f test_output.json ]; then
    echo "✓ Scan completed and output generated"
else
    echo "✗ Scan failed"
    exit 1
fi

# Test 3: Validate JSON
if python3 -m json.tool test_output.json > /dev/null 2>&1; then
    echo "✓ Valid JSON output"
else
    echo "✗ Invalid JSON output"
    exit 1
fi

echo "All tests passed!"
rm test_output.json
```

## Reporting Issues

If you encounter issues:

1. Check this testing guide first
2. Verify all dependencies are installed
3. Test with example.com first
4. Check system logs
5. Document the exact error message
6. Note your system configuration

## Security Testing Notes

### Responsible Testing

- Always obtain written authorization
- Document all testing activities
- Respect rate limits
- Avoid aggressive scanning
- Report findings responsibly

### Test Environment Setup

For learning and testing, consider:

1. **Local VMs**: Set up vulnerable VMs (DVWA, WebGoat)
2. **Docker Containers**: Run test applications locally
3. **Cloud Sandboxes**: Use isolated cloud environments
4. **Bug Bounty Programs**: Test on authorized platforms

## Continuous Testing

### Regular Validation

```bash
# Weekly validation scan
xgenie scan example.com --output validation_$(date +%Y%m%d).json

# Compare results over time
# Ensure consistent functionality
```

### Update Testing

After updates:
1. Test basic functionality
2. Verify all modules work
3. Check for regressions
4. Validate output format
