#!/bin/bash
# Build xGenie .deb package on Linux

set -e

echo "==========================================================="
echo "  xGenie .deb Package Builder (Linux)"
echo "==========================================================="
echo ""

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "[!] This script must be run on a Linux system"
    exit 1
fi

# Check for dpkg-deb
if ! command -v dpkg-deb &> /dev/null; then
    echo "[!] dpkg-deb not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y dpkg-dev
fi

# Check if package structure exists
if [ ! -d "build/debian" ]; then
    echo "[!] Package structure not found. Running build_package.py..."
    python3 build_package.py
fi

# Create dist directory
mkdir -p dist

# Build the package
echo "[*] Building .deb package..."
dpkg-deb --build build/debian dist/xgenie_1.0.0_all.deb

# Check if build was successful
if [ -f "dist/xgenie_1.0.0_all.deb" ]; then
    echo ""
    echo "[+] Package built successfully!"
    echo ""
    echo "Package: dist/xgenie_1.0.0_all.deb"
    echo "Size: $(du -h dist/xgenie_1.0.0_all.deb | cut -f1)"
    echo ""
    echo "To install:"
    echo "  sudo dpkg -i dist/xgenie_1.0.0_all.deb"
    echo "  sudo apt-get install -f"
    echo ""
    echo "To verify:"
    echo "  dpkg -c dist/xgenie_1.0.0_all.deb  # List contents"
    echo "  dpkg -I dist/xgenie_1.0.0_all.deb  # Show info"
    echo ""
else
    echo "[!] Build failed"
    exit 1
fi
