#!/bin/bash

# Setup script for Cloudflare Bypass Tool
set -e

echo "[*] Starting setup process..."

# Update package lists
echo "[*] Updating package lists..."
sudo apt update

# Install system dependencies
echo "[*] Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl

# Create project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

# Verify installation
echo "[*] Verifying installation..."
python3 -c "
import sys
sys.path.append('src')
import requests
import yaml
import aiohttp
print('All dependencies installed successfully')
"

echo "[+] Setup completed successfully!"
echo "[*] To activate the environment, run: source venv/bin/activate"
echo "[*] To run the tool: python3 src/main.py -d example.com"
