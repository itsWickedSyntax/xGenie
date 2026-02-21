#!/usr/bin/env python3
"""
xGenie .deb Package Builder
Creates a Debian package structure for xGenie
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

VERSION = "1.0.0"
ARCH = "all"
PKG_NAME = "xgenie"

def create_directory_structure():
    """Create the Debian package directory structure"""
    print("[*] Creating directory structure...")
    
    build_dir = Path("build/debian")
    
    # Clean previous builds
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Create directories
    dirs = [
        build_dir / "DEBIAN",
        build_dir / "usr/local/bin",
        build_dir / "usr/share/xgenie",
        build_dir / "usr/share/applications",
        build_dir / "usr/share/doc/xgenie",
        build_dir / "usr/share/man/man1",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    return build_dir

def create_control_file(build_dir):
    """Create the DEBIAN/control file"""
    print("[*] Creating control file...")
    
    control_content = f"""Package: {PKG_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: {ARCH}
Depends: python3 (>= 3.8), python3-pip, nmap
Maintainer: xGenie Team <team@xgenie.local>
Description: Security Intelligence Platform
 Production-ready website and infrastructure reconnaissance platform
 for authorized defensive security operations.
 .
 Features:
  - WHOIS & ownership intelligence
  - Port scanning & service discovery
  - Technology stack detection
  - DNS intelligence
  - Admin panel discovery
  - Security analysis
  - Advanced XSS detection engine
"""
    
    control_file = build_dir / "DEBIAN/control"
    control_file.write_text(control_content, encoding='utf-8')

def create_postinst_script(build_dir):
    """Create the post-installation script"""
    print("[*] Creating postinst script...")
    
    postinst_content = """#!/bin/bash
set -e

echo "Installing xGenie dependencies..."

# Install Python dependencies
cd /usr/share/xgenie
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

# Create symlink if not exists
if [ ! -L /usr/local/bin/xgenie ]; then
    ln -sf /usr/share/xgenie/xgenie.sh /usr/local/bin/xgenie
fi

echo ""
echo "==========================================================="
echo "  xGenie Security Intelligence Platform"
echo "==========================================================="
echo ""
echo "[+] Installation complete!"
echo ""
echo "Usage:"
echo "  xgenie scan <target>              # Basic scan"
echo "  xgenie scan <target> --full       # Full scan with XSS"
echo "  xgenie server --port 5000         # Web interface"
echo ""
echo "[!] AUTHORIZED USE ONLY"
echo "    See /usr/share/doc/xgenie/LEGAL_NOTICE.txt"
echo ""
echo "==========================================================="
"""
    
    postinst_file = build_dir / "DEBIAN/postinst"
    postinst_file.write_text(postinst_content, encoding='utf-8')
    postinst_file.chmod(0o755)

def create_prerm_script(build_dir):
    """Create the pre-removal script"""
    print("[*] Creating prerm script...")
    
    prerm_content = """#!/bin/bash
set -e

echo "Removing xGenie..."

# Remove symlink
if [ -L /usr/local/bin/xgenie ]; then
    rm -f /usr/local/bin/xgenie
fi
"""
    
    prerm_file = build_dir / "DEBIAN/prerm"
    prerm_file.write_text(prerm_content, encoding='utf-8')
    prerm_file.chmod(0o755)

def copy_application_files(build_dir):
    """Copy application files to package"""
    print("[*] Copying application files...")
    
    app_dir = build_dir / "usr/share/xgenie"
    
    # Copy backend
    shutil.copytree("backend", app_dir / "backend")
    
    # Copy frontend
    shutil.copytree("frontend", app_dir / "frontend")
    
    # Copy configuration files
    shutil.copy("requirements.txt", app_dir)
    shutil.copy("setup.py", app_dir)
    
    # Copy documentation
    doc_dir = build_dir / "usr/share/doc/xgenie"
    docs = [
        "README.md", "ARCHITECTURE.md", "FEATURES.md", 
        "INSTALL.md", "USAGE_EXAMPLES.md", "TEST_GUIDE.md",
        "LEGAL_NOTICE.txt", "LICENSE"
    ]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy(doc, doc_dir)

def create_launcher_script(build_dir):
    """Create the main launcher script"""
    print("[*] Creating launcher script...")
    
    launcher_content = """#!/bin/bash
# xGenie launcher script

INSTALL_DIR="/usr/share/xgenie"

# Check if running from install directory
if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR"
    python3 -m backend.cli "$@"
else
    echo "Error: xGenie installation not found"
    exit 1
fi
"""
    
    launcher_file = build_dir / "usr/share/xgenie/xgenie.sh"
    launcher_file.write_text(launcher_content, encoding='utf-8')
    launcher_file.chmod(0o755)

def create_desktop_file(build_dir):
    """Create desktop application file"""
    print("[*] Creating desktop file...")
    
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=xGenie
Comment=Security Intelligence Platform
Exec=xgenie server
Icon=security
Terminal=true
Categories=Network;Security;
Keywords=security;reconnaissance;scanning;
"""
    
    desktop_file = build_dir / "usr/share/applications/xgenie.desktop"
    desktop_file.write_text(desktop_content, encoding='utf-8')

def create_man_page(build_dir):
    """Create man page"""
    print("[*] Creating man page...")
    
    man_content = """.TH XGENIE 1 "2024" "xGenie 1.0.0" "User Commands"
.SH NAME
xgenie \\- Security Intelligence Platform
.SH SYNOPSIS
.B xgenie
.I scan
.I <target>
[OPTIONS]
.br
.B xgenie
.I server
[OPTIONS]
.SH DESCRIPTION
xGenie is a production-ready website and infrastructure reconnaissance platform
for authorized defensive security operations.
.SH OPTIONS
.TP
.B scan <target>
Perform reconnaissance scan on target domain or IP
.TP
.B --full
Perform full scan including XSS detection (slower)
.TP
.B --output, -o <file>
Save results to JSON file
.TP
.B server
Start web interface
.TP
.B --port <port>
Specify server port (default: 5000)
.SH EXAMPLES
.TP
Basic scan:
.B xgenie scan example.com
.TP
Full scan with output:
.B xgenie scan example.com --full --output results.json
.TP
Start web server:
.B xgenie server --port 8080
.SH LEGAL
This tool is for AUTHORIZED USE ONLY. Users must obtain proper authorization
before scanning any systems. Unauthorized access is illegal.
.SH AUTHOR
xGenie Team
.SH SEE ALSO
Full documentation: /usr/share/doc/xgenie/
"""
    
    man_file = build_dir / "usr/share/man/man1/xgenie.1"
    man_file.write_text(man_content, encoding='utf-8')

def build_package(build_dir):
    """Build the .deb package"""
    print("[*] Building .deb package...")
    
    # Create dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    package_name = f"{PKG_NAME}_{VERSION}_{ARCH}.deb"
    package_path = dist_dir / package_name
    
    # Build package using dpkg-deb
    try:
        subprocess.run(
            ["dpkg-deb", "--build", str(build_dir), str(package_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[+] Package built successfully: {package_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error building package: {e.stderr}")
        return False
    except FileNotFoundError:
        print("[!] dpkg-deb not found. Creating package structure only.")
        print("[!] Run this script on a Debian/Ubuntu system to build the .deb")
        return False

def create_install_instructions():
    """Create installation instructions"""
    print("[*] Creating installation instructions...")
    
    instructions = """
===========================================================
  xGenie Package Build Complete
===========================================================

Package structure created in: build/debian/

To build the .deb package on Linux:
  1. Transfer this directory to a Debian/Ubuntu system
  2. Run: dpkg-deb --build build/debian dist/xgenie_1.0.0_all.deb

To install:
  sudo dpkg -i dist/xgenie_1.0.0_all.deb
  sudo apt-get install -f  # Fix dependencies if needed

To use:
  xgenie scan example.com
  xgenie server --port 5000

===========================================================
"""
    
    Path("BUILD_INSTRUCTIONS.txt").write_text(instructions, encoding='utf-8')
    print(instructions)

def main():
    print("===========================================================")
    print("  xGenie .deb Package Builder")
    print("===========================================================")
    print()
    
    try:
        # Create package structure
        build_dir = create_directory_structure()
        create_control_file(build_dir)
        create_postinst_script(build_dir)
        create_prerm_script(build_dir)
        copy_application_files(build_dir)
        create_launcher_script(build_dir)
        create_desktop_file(build_dir)
        create_man_page(build_dir)
        
        # Try to build package
        success = build_package(build_dir)
        
        # Create instructions
        create_install_instructions()
        
        if success:
            print("\n[+] Package ready for installation!")
        else:
            print("\n[!] Package structure created. Build on Linux to create .deb")
        
        return 0
        
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
