#!/bin/bash
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
