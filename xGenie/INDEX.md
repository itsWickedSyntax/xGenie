# xGenie Project Index

## 📁 Quick Navigation

This document helps you find what you need quickly.

---

## 🚀 Getting Started

**New to xGenie? Start here:**

1. [README.md](README.md) - Project overview and quick start
2. [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md) - Build the .deb package
3. [INSTALL.md](INSTALL.md) - Installation instructions
4. [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - How to use xGenie

---

## 📦 Building the Package

**Want to build the .deb file?**

- [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md) - **START HERE** - Complete build guide
- [build_on_linux.sh](build_on_linux.sh) - Automated build script (Linux)
- [build_package.py](build_package.py) - Python package builder
- [BUILD_INSTRUCTIONS.txt](BUILD_INSTRUCTIONS.txt) - Quick build instructions
- [PACKAGE_README.md](PACKAGE_README.md) - Package documentation

---

## 📚 Documentation

### User Documentation
- [README.md](README.md) - Main documentation
- [INSTALL.md](INSTALL.md) - Installation guide
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Usage examples and scenarios
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference card
- [TEST_GUIDE.md](TEST_GUIDE.md) - Testing procedures

### Technical Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [FEATURES.md](FEATURES.md) - Complete feature list
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

### Package Documentation
- [DEBIAN_PACKAGE_COMPLETE.md](DEBIAN_PACKAGE_COMPLETE.md) - Package status
- [PACKAGE_README.md](PACKAGE_README.md) - Package details
- [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md) - Build instructions

### Project Status
- [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) - Completion checklist
- [FINAL_SUMMARY.md](FINAL_SUMMARY.md) - Final project summary

### Legal
- [LEGAL_NOTICE.txt](LEGAL_NOTICE.txt) - Legal and ethical guidelines
- [LICENSE](LICENSE) - MIT License

---

## 💻 Source Code

### Backend (Python)
```
backend/
├── cli.py                          # Command-line interface
├── server.py                       # Flask web server
├── core/
│   ├── scanner.py                  # Main scan orchestrator
│   └── reporter.py                 # Results formatting
└── modules/
    ├── whois_intel.py              # WHOIS lookups
    ├── dns_intel.py                # DNS enumeration
    ├── port_scanner.py             # Port scanning
    ├── tech_detector.py            # Technology detection
    ├── admin_finder.py             # Admin panel discovery
    ├── security_analyzer.py        # Security analysis
    └── xss_engine/
        ├── crawler.py              # Dynamic web crawler
        ├── parameter_mapper.py     # Attack surface mapping
        ├── reflection_tester.py    # Reflection testing
        ├── context_classifier.py   # Context classification
        ├── dom_analyzer.py         # DOM sink detection
        ├── risk_scorer.py          # Risk scoring
        └── xss_scanner.py          # XSS orchestrator
```

### Frontend (Web Interface)
```
frontend/
├── templates/
│   └── index.html                  # Main UI
└── static/
    ├── css/style.css               # Styling
    └── js/app.js                   # Frontend logic
```

---

## 🔧 Configuration Files

- [requirements.txt](requirements.txt) - Python dependencies
- [setup.py](setup.py) - Package setup configuration
- [.gitignore](.gitignore) - Git exclusions

---

## 🛠️ Build Scripts

- [build_on_linux.sh](build_on_linux.sh) - **Main build script** (Linux)
- [build_package.py](build_package.py) - Python package builder
- [build_deb.sh](build_deb.sh) - Original build script
- [verify_installation.sh](verify_installation.sh) - Installation verification

---

## 📋 By Task

### I want to...

**...understand what xGenie does**
→ [README.md](README.md)
→ [FEATURES.md](FEATURES.md)

**...build the .deb package**
→ [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md)
→ [build_on_linux.sh](build_on_linux.sh)

**...install xGenie**
→ [INSTALL.md](INSTALL.md)
→ [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md)

**...use xGenie**
→ [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**...test xGenie**
→ [TEST_GUIDE.md](TEST_GUIDE.md)
→ [verify_installation.sh](verify_installation.sh)

**...understand the architecture**
→ [ARCHITECTURE.md](ARCHITECTURE.md)
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**...know what's implemented**
→ [FEATURES.md](FEATURES.md)
→ [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)

**...understand legal requirements**
→ [LEGAL_NOTICE.txt](LEGAL_NOTICE.txt)
→ [LICENSE](LICENSE)

**...troubleshoot issues**
→ [TEST_GUIDE.md](TEST_GUIDE.md) (Troubleshooting section)
→ [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md) (Troubleshooting section)

---

## 📊 By Role

### For Users
1. [README.md](README.md) - Overview
2. [INSTALL.md](INSTALL.md) - Installation
3. [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Usage
4. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference

### For Developers
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
3. Source code in `backend/` and `frontend/`
4. [requirements.txt](requirements.txt) - Dependencies

### For Package Maintainers
1. [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md) - Build guide
2. [PACKAGE_README.md](PACKAGE_README.md) - Package docs
3. [build_on_linux.sh](build_on_linux.sh) - Build script
4. [DEBIAN_PACKAGE_COMPLETE.md](DEBIAN_PACKAGE_COMPLETE.md) - Status

### For Security Professionals
1. [FEATURES.md](FEATURES.md) - Capabilities
2. [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Scenarios
3. [LEGAL_NOTICE.txt](LEGAL_NOTICE.txt) - Legal requirements
4. [TEST_GUIDE.md](TEST_GUIDE.md) - Testing

---

## 🎯 Quick Commands

### Build Package
```bash
./build_on_linux.sh
```

### Install Package
```bash
sudo dpkg -i dist/xgenie_1.0.0_all.deb
```

### Use xGenie
```bash
xgenie scan example.com
xgenie server --port 5000
```

### Verify Installation
```bash
./verify_installation.sh
```

---

## 📁 Directory Structure

```
xGenie/
├── backend/                    # Python backend (21 files)
├── frontend/                   # Web interface (3 files)
├── build/                      # Build artifacts
│   └── debian/                 # Debian package structure
├── dist/                       # Distribution files
├── Documentation (16 files)    # All .md and .txt files
├── Build Scripts (4 files)     # Build automation
└── Configuration (4 files)     # Project configuration
```

---

## 🔍 Search Tips

### Find by Topic

**WHOIS**: backend/modules/whois_intel.py
**DNS**: backend/modules/dns_intel.py
**Ports**: backend/modules/port_scanner.py
**Technology**: backend/modules/tech_detector.py
**Admin Panels**: backend/modules/admin_finder.py
**Security**: backend/modules/security_analyzer.py
**XSS**: backend/modules/xss_engine/

### Find by File Type

**Python**: `backend/**/*.py`
**HTML**: `frontend/templates/*.html`
**CSS**: `frontend/static/css/*.css`
**JavaScript**: `frontend/static/js/*.js`
**Documentation**: `*.md`, `*.txt`
**Scripts**: `*.sh`, `*.py` (root level)

---

## 📞 Need Help?

1. Check the relevant documentation file above
2. Review [TEST_GUIDE.md](TEST_GUIDE.md) troubleshooting section
3. Check [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md) for build issues
4. Review error messages carefully

---

## ✅ Project Status

- **Application**: Complete ✅
- **Documentation**: Complete ✅
- **Package Structure**: Complete ✅
- **Build Scripts**: Complete ✅
- **Ready for**: Building on Linux ⏳

---

## 🎉 Quick Start Path

1. Read [README.md](README.md)
2. Follow [HOW_TO_BUILD_DEB.md](HOW_TO_BUILD_DEB.md)
3. Run `./build_on_linux.sh`
4. Install with `sudo dpkg -i dist/xgenie_1.0.0_all.deb`
5. Use with `xgenie scan example.com`

---

**Total Files**: 87 files
**Documentation Files**: 16 files
**Source Code Files**: 24 files
**Build Files**: 4 files
**Configuration Files**: 4 files

---

*Last Updated: Project Complete*
*Version: 1.0.0*
*Status: Ready for Deployment*
