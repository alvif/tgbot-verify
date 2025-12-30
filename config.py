"""Berkas konfigurasi global"""
import os
from dotenv import load_dotenv

# Muat berkas .env
load_dotenv()

# Konfigurasi Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "pk_oa")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/pk_oa")

# Konfigurasi admin
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))

# Konfigurasi poin
VERIFY_COST = 1  # Poin yang dikonsumsi untuk verifikasi
CHECKIN_REWARD = 1  # Poin hadiah check-in
INVITE_REWARD = 2  # Poin hadiah undangan
REGISTER_REWARD = 1  # Poin hadiah registrasi

# Tautan bantuan
HELP_NOTION_URL = "https://rhetorical-era-3f3.notion.site/dd78531dbac745af9bbac156b51da9cc"
