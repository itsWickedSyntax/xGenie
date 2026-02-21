# xGenie Usage Examples

## CLI Examples

### Basic Reconnaissance

```bash
# Scan a domain
xgenie scan example.com

# Scan an IP address
xgenie scan 192.168.1.1

# Full scan with XSS detection (slower but comprehensive)
xgenie scan example.com --full
```

### Output Options

```bash
# Save results to JSON
xgenie scan example.com --output scan_results.json

# Full scan with output
xgenie scan example.com --full --output full_scan.json
```

### Web Server Mode

```bash
# Start web interface on default port (5000)
xgenie server

# Start on custom port
xgenie server --port 8080

# Access at http://localhost:5000
```

## Web Interface Usage

1. Open browser to `http://localhost:5000`
2. Enter target domain or IP
3. Check "Deep Scan" for XSS detection
4. Click "Start Reconnaissance"
5. Monitor real-time progress
6. Review results in organized cards
7. Export to JSON if needed

## Example Scan Output

### WHOIS Intelligence
```
Registrar: GoDaddy.com, LLC
Organization: Example Corp
Country: US
Created: 2020-01-15
Expires: 2025-01-15
```

### DNS Records
```
A Records: 93.184.216.34
MX Records: 10 mail.example.com
NS Records: ns1.example.com, ns2.example.com
SPF: v=spf1 include:_spf.example.com ~all
```

### Open Ports
```
Port  Service  Banner
22    ssh      OpenSSH 8.2p1
80    http     nginx/1.18.0
443   https    nginx/1.18.0
```

### Technology Stack
```
Web Server: nginx/1.18.0
CMS: WordPress
Frameworks: PHP
JS Libraries: jQuery, Bootstrap
CDN: Cloudflare
```

### Security Analysis
```
Risk Score: 45/100 (Medium)
Missing Headers: 3
  - Strict-Transport-Security
  - Content-Security-Policy
  - X-Frame-Options
Vulnerabilities: 5 found
```

### XSS Detection (Deep Scan)
```
Endpoints Tested: 15
Total Vulnerabilities: 2
Reflected XSS: 1
DOM-based XSS: 1
High Risk: 1
```

## Real-World Scenarios

### Scenario 1: Pre-Deployment Security Check

```bash
# Before launching a new website
xgenie scan staging.myapp.com --full --output pre_launch_audit.json

# Review findings
# Fix security issues
# Re-scan to verify
```

### Scenario 2: Periodic Security Monitoring

```bash
# Weekly security scan
xgenie scan production.myapp.com --output weekly_scan_$(date +%Y%m%d).json

# Compare with previous scans
# Track security posture over time
```

### Scenario 3: Incident Response

```bash
# Quick reconnaissance during incident
xgenie scan compromised-site.com

# Identify exposed services
# Check for misconfigurations
# Document findings
```

### Scenario 4: Third-Party Vendor Assessment

```bash
# Assess vendor security posture (with authorization)
xgenie scan vendor-api.example.com --full --output vendor_assessment.json

# Review technology stack
# Identify potential risks
# Make informed decisions
```

## Integration Examples

### Automated Scanning Script

```bash
#!/bin/bash
# automated_scan.sh

TARGETS="site1.com site2.com site3.com"
OUTPUT_DIR="./scan_results"

mkdir -p $OUTPUT_DIR

for target in $TARGETS; do
    echo "Scanning $target..."
    xgenie scan $target --output "$OUTPUT_DIR/${target}_$(date +%Y%m%d).json"
done

echo "All scans completed"
```

### CI/CD Integration

```yaml
# .gitlab-ci.yml example
security_scan:
  stage: test
  script:
    - xgenie scan staging.myapp.com --output security_scan.json
  artifacts:
    paths:
      - security_scan.json
  only:
    - main
```

## Best Practices

1. **Always Get Authorization**
   - Obtain written permission before scanning
   - Document authorization
   - Respect scope limitations

2. **Start with Basic Scans**
   - Use basic scan first for quick overview
   - Use --full only when needed
   - Deep scans take longer

3. **Save Results**
   - Always use --output for documentation
   - Include timestamps in filenames
   - Archive results for comparison

4. **Rate Limiting**
   - Be respectful of target resources
   - Avoid aggressive scanning
   - Use appropriate scan depth

5. **Review Findings**
   - Analyze all results carefully
   - Verify vulnerabilities manually
   - Prioritize by risk score

6. **Document Everything**
   - Keep scan logs
   - Document authorization
   - Track remediation efforts
