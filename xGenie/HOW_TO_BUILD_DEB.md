# How to Build the xGenie .deb Package

## Quick Start

The package structure is ready. You just need to build it on a Linux system.

### Fastest Method (Linux/WSL)

```bash
chmod +x build_on_linux.sh
./build_on_linux.sh
```

That's it! The .deb file will be created in `dist/xgenie_1.0.0_all.deb`

---

## Detailed Instructions

### Method 1: Using WSL (Windows Subsystem for Linux)

If you're on Windows with WSL installed:

```bash
# 1. Open WSL terminal
wsl

# 2. Navigate to project directory
cd /mnt/c/Users/HP/Desktop/New\ folder/

# 3. Make build script executable
chmod +x build_on_linux.sh

# 4. Run build script
./build_on_linux.sh

# 5. The .deb file will be in dist/
ls -lh dist/xgenie_1.0.0_all.deb
```

### Method 2: Transfer to Linux System

```bash
# 1. On Windows, compress the project
# (Use 7-Zip, WinRAR, or built-in compression)

# 2. Transfer to Linux (via USB, network, etc.)
scp -r "New folder" user@linux-host:/home/user/xgenie/

# 3. On Linux, navigate to directory
ssh user@linux-host
cd /home/user/xgenie/

# 4. Build the package
chmod +x build_on_linux.sh
./build_on_linux.sh
```

### Method 3: Using Python Builder

```bash
# On Linux/WSL
python3 build_package.py

# This will:
# - Create package structure (already done)
# - Build .deb file
# - Place it in dist/
```

### Method 4: Manual Build

```bash
# If you want to build manually
mkdir -p dist
dpkg-deb --build build/debian dist/xgenie_1.0.0_all.deb
```

---

## Prerequisites

### On Linux System

```bash
# Install required tools
sudo apt-get update
sudo apt-get install -y dpkg-dev python3

# Verify installation
dpkg-deb --version
python3 --version
```

### On WSL

```bash
# Install WSL if not already installed (Windows PowerShell as Admin)
wsl --install

# Or install specific distribution
wsl --install -d Ubuntu

# Then follow Linux instructions above
```

---

## Verification

### Before Building

```bash
# Check package structure exists
ls -la build/debian/

# Should show:
# - DEBIAN/ directory
# - usr/ directory
```

### After Building

```bash
# Check .deb file was created
ls -lh dist/xgenie_1.0.0_all.deb

# View package contents
dpkg -c dist/xgenie_1.0.0_all.deb

# View package information
dpkg -I dist/xgenie_1.0.0_all.deb

# Expected output:
# Package: xgenie
# Version: 1.0.0
# Architecture: all
# Depends: python3 (>= 3.8), python3-pip, nmap
```

---

## Installation

### Install the Package

```bash
# Install
sudo dpkg -i dist/xgenie_1.0.0_all.deb

# Fix dependencies if needed
sudo apt-get install -f

# Verify installation
which xgenie
xgenie --help
```

### Test the Installation

```bash
# Run basic scan
xgenie scan example.com

# Start web server
xgenie server --port 5000

# View man page
man xgenie
```

---

## Troubleshooting

### Build Issues

**Problem**: `dpkg-deb: command not found`

```bash
# Solution: Install dpkg-dev
sudo apt-get update
sudo apt-get install dpkg-dev
```

**Problem**: `Permission denied` when running build script

```bash
# Solution: Make script executable
chmod +x build_on_linux.sh
```

**Problem**: Package structure not found

```bash
# Solution: Run Python builder first
python3 build_package.py
```

### Installation Issues

**Problem**: Dependency errors during installation

```bash
# Solution: Fix dependencies
sudo apt-get install -f
```

**Problem**: Python dependencies fail to install

```bash
# Solution: Install manually
cd /usr/share/xgenie
sudo pip3 install -r requirements.txt
```

**Problem**: `xgenie: command not found` after installation

```bash
# Solution: Check symlink
ls -la /usr/local/bin/xgenie

# Recreate if needed
sudo ln -sf /usr/share/xgenie/xgenie.sh /usr/local/bin/xgenie
sudo chmod +x /usr/local/bin/xgenie
```

---

## Build Output

### Expected Output

```
===========================================================
  xGenie .deb Package Builder (Linux)
===========================================================

[*] Building .deb package...

[+] Package built successfully!

Package: dist/xgenie_1.0.0_all.deb
Size: 1.2M

To install:
  sudo dpkg -i dist/xgenie_1.0.0_all.deb
  sudo apt-get install -f

To verify:
  dpkg -c dist/xgenie_1.0.0_all.deb  # List contents
  dpkg -I dist/xgenie_1.0.0_all.deb  # Show info
```

### Package Contents

The .deb file will contain:

```
/usr/local/bin/                     # Symlink to executable
/usr/share/xgenie/                  # Application files
  ├── backend/                      # Python backend
  ├── frontend/                     # Web interface
  ├── requirements.txt              # Dependencies
  └── xgenie.sh                     # Launcher script
/usr/share/doc/xgenie/              # Documentation
  ├── README.md
  ├── ARCHITECTURE.md
  ├── FEATURES.md
  ├── INSTALL.md
  ├── USAGE_EXAMPLES.md
  ├── TEST_GUIDE.md
  ├── LEGAL_NOTICE.txt
  └── LICENSE
/usr/share/man/man1/                # Man page
  └── xgenie.1
/usr/share/applications/            # Desktop entry
  └── xgenie.desktop
```

---

## Alternative: Manual Installation

If you can't build the .deb package, you can install manually:

```bash
# 1. Install system dependencies
sudo apt-get install python3 python3-pip nmap

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Create launcher script
cat > /tmp/xgenie << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 -m backend.cli "$@"
EOF

# 4. Install launcher
sudo mv /tmp/xgenie /usr/local/bin/xgenie
sudo chmod +x /usr/local/bin/xgenie

# 5. Test
xgenie scan example.com
```

---

## Distribution

### Share the .deb File

Once built, you can distribute the .deb file:

```bash
# Create checksum
sha256sum dist/xgenie_1.0.0_all.deb > dist/xgenie_1.0.0_all.deb.sha256

# Upload to GitHub releases
# Or share directly with users
```

### Installation Instructions for Users

```bash
# Download the .deb file
wget https://example.com/xgenie_1.0.0_all.deb

# Verify checksum (optional)
sha256sum -c xgenie_1.0.0_all.deb.sha256

# Install
sudo dpkg -i xgenie_1.0.0_all.deb
sudo apt-get install -f

# Use
xgenie scan example.com
```

---

## Summary

### What You Have Now
✅ Complete package structure in `build/debian/`
✅ All application files included
✅ Build scripts ready
✅ Documentation complete

### What You Need to Do
1. Run build script on Linux/WSL
2. Get .deb file from `dist/` directory
3. Install and test
4. Distribute to users

### One Command Build
```bash
./build_on_linux.sh
```

That's all you need!

---

## Support

If you encounter issues:

1. Check this guide
2. Review BUILD_INSTRUCTIONS.txt
3. Check PACKAGE_README.md
4. Review error messages carefully
5. Ensure you're on a Debian/Ubuntu system

---

**Ready to build? Run: `./build_on_linux.sh`**
