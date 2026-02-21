#!/bin/bash

# xGenie Installation Verification Script

echo "═══════════════════════════════════════════════════════════"
echo "  xGenie Installation Verification"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
PASSED=0
FAILED=0

# Function to check
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1"
        ((FAILED++))
    fi
}

# 1. Check Python version
echo "Checking Python..."
python3 --version > /dev/null 2>&1
check "Python 3 installed"

# 2. Check pip
pip3 --version > /dev/null 2>&1
check "pip3 installed"

# 3. Check nmap
which nmap > /dev/null 2>&1
check "nmap installed"

# 4. Check project structure
echo ""
echo "Checking project structure..."

[ -d "backend" ]
check "backend/ directory exists"

[ -d "backend/core" ]
check "backend/core/ directory exists"

[ -d "backend/modules" ]
check "backend/modules/ directory exists"

[ -d "backend/modules/xss_engine" ]
check "backend/modules/xss_engine/ directory exists"

[ -d "frontend" ]
check "frontend/ directory exists"

[ -d "frontend/templates" ]
check "frontend/templates/ directory exists"

[ -d "frontend/static" ]
check "frontend/static/ directory exists"

# 5. Check core files
echo ""
echo "Checking core files..."

[ -f "backend/cli.py" ]
check "backend/cli.py exists"

[ -f "backend/server.py" ]
check "backend/server.py exists"

[ -f "backend/core/scanner.py" ]
check "backend/core/scanner.py exists"

[ -f "backend/core/reporter.py" ]
check "backend/core/reporter.py exists"

# 6. Check modules
echo ""
echo "Checking intelligence modules..."

[ -f "backend/modules/whois_intel.py" ]
check "whois_intel.py exists"

[ -f "backend/modules/dns_intel.py" ]
check "dns_intel.py exists"

[ -f "backend/modules/port_scanner.py" ]
check "port_scanner.py exists"

[ -f "backend/modules/tech_detector.py" ]
check "tech_detector.py exists"

[ -f "backend/modules/admin_finder.py" ]
check "admin_finder.py exists"

[ -f "backend/modules/security_analyzer.py" ]
check "security_analyzer.py exists"

# 7. Check XSS engine
echo ""
echo "Checking XSS detection engine..."

[ -f "backend/modules/xss_engine/crawler.py" ]
check "crawler.py exists"

[ -f "backend/modules/xss_engine/parameter_mapper.py" ]
check "parameter_mapper.py exists"

[ -f "backend/modules/xss_engine/reflection_tester.py" ]
check "reflection_tester.py exists"

[ -f "backend/modules/xss_engine/context_classifier.py" ]
check "context_classifier.py exists"

[ -f "backend/modules/xss_engine/dom_analyzer.py" ]
check "dom_analyzer.py exists"

[ -f "backend/modules/xss_engine/risk_scorer.py" ]
check "risk_scorer.py exists"

[ -f "backend/modules/xss_engine/xss_scanner.py" ]
check "xss_scanner.py exists"

# 8. Check frontend
echo ""
echo "Checking frontend files..."

[ -f "frontend/templates/index.html" ]
check "index.html exists"

[ -f "frontend/static/css/style.css" ]
check "style.css exists"

[ -f "frontend/static/js/app.js" ]
check "app.js exists"

# 9. Check configuration files
echo ""
echo "Checking configuration files..."

[ -f "requirements.txt" ]
check "requirements.txt exists"

[ -f "setup.py" ]
check "setup.py exists"

[ -f "build_deb.sh" ]
check "build_deb.sh exists"

# 10. Check documentation
echo ""
echo "Checking documentation..."

[ -f "README.md" ]
check "README.md exists"

[ -f "ARCHITECTURE.md" ]
check "ARCHITECTURE.md exists"

[ -f "FEATURES.md" ]
check "FEATURES.md exists"

[ -f "INSTALL.md" ]
check "INSTALL.md exists"

[ -f "USAGE_EXAMPLES.md" ]
check "USAGE_EXAMPLES.md exists"

[ -f "TEST_GUIDE.md" ]
check "TEST_GUIDE.md exists"

[ -f "LEGAL_NOTICE.txt" ]
check "LEGAL_NOTICE.txt exists"

[ -f "LICENSE" ]
check "LICENSE exists"

# 11. Check Python syntax
echo ""
echo "Checking Python syntax..."

python3 -m py_compile backend/cli.py 2>/dev/null
check "cli.py syntax valid"

python3 -m py_compile backend/server.py 2>/dev/null
check "server.py syntax valid"

python3 -m py_compile backend/core/scanner.py 2>/dev/null
check "scanner.py syntax valid"

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Verification Summary"
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! xGenie is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Install dependencies: pip3 install -r requirements.txt"
    echo "  2. Build package: ./build_deb.sh"
    echo "  3. Install: sudo dpkg -i dist/xgenie_1.0.0_amd64.deb"
    echo "  4. Run: xgenie scan example.com"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the output above.${NC}"
    exit 1
fi
