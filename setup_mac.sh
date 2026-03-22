#!/bin/bash
echo "🍎 Mapple v0.2.0 Mac Installer"
echo "---------------------------"

# 1. Python Check
if ! command -v python3 &> /dev/null
then
    echo "[!] Python 3 was not found."
    echo "[!] Opening download page: https://www.python.org/downloads/macos/"
    open https://www.python.org/downloads/macos/
    exit
fi

# 2. Permissions (Assuming you renamed mppl.sh to mppl)
if [ -f "./mppl" ]; then
    chmod +x ./mppl
    echo "[*] Permissions set for 'mppl' runner."
else
    echo "[!] Error: Could not find the 'mppl' file in this folder."
    exit
fi

# 3. Path Automation
# This checks if the current folder is already in the path to avoid duplicates
if [[ ":$PATH:" != *":$(pwd):"* ]]; then
    # Detect shell (zsh is default, but some use bash)
    SHELL_CONF="$HOME/.zshrc"
    if [ ! -f "$SHELL_CONF" ]; then SHELL_CONF="$HOME/.bash_profile"; fi
    
    echo "export PATH=\"\$PATH:$(pwd)\"" >> "$SHELL_CONF"
    echo "[*] Added to $SHELL_CONF"
    echo "🚀 Setup Complete! Run 'source $SHELL_CONF' to refresh your terminal."
else
    echo "[OK] Mapple is already in your PATH."
fi

echo "---------------------------"
echo "Try running: mppl --doctor"