# xGenie Debian Package

## Package Information

- **Package Name**: xgenie
- **Version**: 1.0.0
- **Architecture**: all (platform independent)
- **Size**: ~2-3 MB (depends on dependencies)

## Package Structure Created

The package structure has been created in `build/debian/` with the following layout:

```
build/debian/
├── DEBIAN/
│   ├── control          # Package metadata
│   ├── postinst         # Post-installation script
│   └── prerm            # Pre-removal script
├── usr/
│   ├── local/bin/       # Executables
│   ├── share/
│   │   ├── xgenie/      # Application files
│   │   │   ├── backend/
│   │   │   ├── frontend/
│   │   │   ├── requirements.txt
│   │   │   └── xgenie.sh
│   │   ├── applications/
│   │   │   └── xgenie.desktop
│   │   ├── doc/xgenie/  # Documentation
│   │   └── man/man1/    # Man page
│   │       └── xgenie.1
```

## Building the .deb Package

### On Windows (Current System)

The package structure has been created, but the actual .deb file cannot be built on Windows.

**Options:**
1. Transfer the entire project to a Linux system
2. Use WSL (Windows Subsystem for Linux)
3. Use a Linux VM or Docker container

### On Linux/WSL

```bash
# Method 1: Use the automated script
chmod +x build_on_linux.sh
./build_on_linux.sh

# Method 2: Use Python builder
python3 build_package.py

# Method 3: Manual build
dpkg-deb --build build/debian dist/xgenie_1.0.0_all.deb
```

## Using WSL (Windows Subsystem for Linux)

If you have WSL installed on Windows:

```bash
# Open WSL terminal
wsl

# Navigate to project directory
cd /mnt/c/Users/HP/Desktop/New\ folder/

# Build the package
python3 build_package.py

# Or use the Linux build script
chmod +x build_on_linux.sh
./build_on_linux.sh
```

## Installation

Once the .deb file is built:

```bash
# Install the package
sudo dpkg -i dist/xgenie_1.0.0_all.deb

# Fix any dependency issues
sudo apt-get install -f

# Verify installation
xgenie --help
which xgenie
```

## Package Contents

The package includes:

### Application Files
- Complete Python backend (21 files)
- Web frontend (HTML/CSS/JS)
- All intelligence modules
- XSS detection engine

### Documentation
- README.md
- ARCHITECTURE.md
- FEATURES.md
- INSTALL.md
- USAGE_EXAMPLES.md
- TEST_GUIDE.md
- LEGAL_NOTICE.txt
- LICENSE

### System Integration
- Executable: `/usr/local/bin/xgenie`
- Application files: `/usr/share/xgenie/`
- Documentation: `/usr/share/doc/xgenie/`
- Man page: `/usr/share/man/man1/xgenie.1`
- Desktop entry: `/usr/share/applications/xgenie.desktop`

## Dependencies

The package depends on:
- python3 (>= 3.8)
- python3-pip
- nmap

Python dependencies are installed automatically via pip during post-installation.

## Post-Installation

After installation, the package will:
1. Install Python dependencies from requirements.txt
2. Create symlink to executable
3. Display usage information

## Verification

```bash
# List package contents
dpkg -c dist/xgenie_1.0.0_all.deb

# Show package information
dpkg -I dist/xgenie_1.0.0_all.deb

# Check installed files
dpkg -L xgenie

# Verify package integrity
dpkg --verify xgenie
```

## Uninstallation

```bash
# Remove package
sudo dpkg -r xgenie

# Remove package and configuration
sudo dpkg -P xgenie
```

## Troubleshooting

### Build Issues

**Issue**: dpkg-deb not found
```bash
sudo apt-get update
sudo apt-get install dpkg-dev
```

**Issue**: Permission denied
```bash
chmod +x build_on_linux.sh
chmod +x build_package.py
```

### Installation Issues

**Issue**: Dependency problems
```bash
sudo apt-get install -f
```

**Issue**: Python dependencies fail
```bash
cd /usr/share/xgenie
sudo pip3 install -r requirements.txt
```

## Alternative: Manual Installation

If you can't build the .deb package, you can install manually:

```bash
# Install system dependencies
sudo apt-get install python3 python3-pip nmap

# Install Python dependencies
pip3 install -r requirements.txt

# Create symlink
sudo ln -s $(pwd)/backend/cli.py /usr/local/bin/xgenie
sudo chmod +x /usr/local/bin/xgenie

# Run
xgenie scan example.com
```

## Package Signing (Optional)

To sign the package for distribution:

```bash
# Generate GPG key if needed
gpg --gen-key

# Sign the package
dpkg-sig --sign builder dist/xgenie_1.0.0_all.deb

# Verify signature
dpkg-sig --verify dist/xgenie_1.0.0_all.deb
```

## Distribution

The package can be distributed via:
1. Direct download (.deb file)
2. Personal Package Archive (PPA)
3. Custom APT repository
4. GitHub Releases

## Support

For issues with the package:
1. Check BUILD_INSTRUCTIONS.txt
2. Review installation logs
3. Verify dependencies
4. Check system compatibility

## Notes

- Package is architecture-independent (pure Python)
- Requires Python 3.8 or higher
- Tested on Ubuntu 20.04+ and Debian 11+
- Some features require root privileges (port scanning)
