#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[92m📦 Telegram Auto Group Creator - O‘rnatilmoqda...\033[0m"

pkg update -y && pkg upgrade -y
pkg install python git termux-api -y

pip install --upgrade pip
pip install telethon

echo -e "\n\033[93m✅ O‘rnatish tugadi! Dastur ishga tushmoqda...\033[0m"
python avtoguruh.py
