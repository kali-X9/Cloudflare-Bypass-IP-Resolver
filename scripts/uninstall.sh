#!/bin/bash

# Uninstallation script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Remove virtual environment
if [ -d "venv" ]; then
    echo "[*] Removing virtual environment..."
    rm -rf venv
fi

# Remove logs
if [ -d "logs" ]; then
    echo "[*] Removing log files..."
    rm -rf logs
fi

echo "[+] Uninstallation completed!"
