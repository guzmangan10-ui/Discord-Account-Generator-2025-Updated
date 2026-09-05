#!/bin/bash
# Discord Generator - Termux Installation

echo "[*] Updating packages..."
pkg update && pkg upgrade -y

echo "[*] Installing Python..."
pkg install python python-pip git -y

echo "[*] Installing dependencies..."
pip install -r requirements.txt

echo "[+] Done! Run: python3 main.py"
