#!/bin/bash

set -e

VERSION="1.0.0"
ARCH="amd64"
PKG_NAME="xgenie"
BUILD_DIR="build/debian"

echo "Building xGenie .deb package..."

# Clean previous builds
rm -rf build dist

# Create directory structure
mkdir -p ${BUILD_DIR}/DEBIAN
mkdir -p ${BUILD_DIR}/usr/local/bin
mkdir -p ${BUILD_DIR}/usr/share/${PKG_NAME}
mkdir -p ${BUILD_DIR}/usr/share/applications
mkdir -p ${BUILD_DIR}/usr/share/doc/${PKG_NAME}

# Create control file
cat > ${BUILD_DIR}/DEBIAN/control << EOF
Package: ${PKG_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.8), python3-pip, nmap
Maintainer: xGenie Team <team@xgenie.local>
Description: Security Intelligence Platform
 Production-ready website and infrastructure reconnaissance platform
 for authorized defensive security operations.
EOF

# Copy application files
cp -r backend ${BUILD_DIR}/usr/share/${PKG_NAME}/
cp -r frontend ${BUILD_DIR}/usr/share/${PKG_NAME}/
cp requirements.txt ${BUILD_DIR}/usr/share/${PKG_NAME}/
cp setup.py ${BUILD_DIR}/usr/share/${PKG_NAME}/
cp README.md ${BUILD_DIR}/usr/share/doc/${PKG_NAME}/

# Create launcher script
cat > ${BUILD_DIR}/usr/local/bin/xgenie << 'EOF'
#!/bin/bash
cd /usr/share/xgenie
python3 -m backend.cli "$@"
EOF

chmod +x ${BUILD_DIR}/usr/local/bin/xgenie

# Create postinst script
cat > ${BUILD_DIR}/DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

cd /usr/share/xgenie
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo "xGenie installed successfully!"
echo "Run: xgenie scan <target>"
EOF

chmod +x ${BUILD_DIR}/DEBIAN/postinst

# Build package
mkdir -p dist
dpkg-deb --build ${BUILD_DIR} dist/${PKG_NAME}_${VERSION}_${ARCH}.deb

echo "Package built: dist/${PKG_NAME}_${VERSION}_${ARCH}.deb"
