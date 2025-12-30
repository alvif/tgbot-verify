"""Script untuk membuat database MySQL"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Koneksi ke MySQL tanpa specify database
conn = pymysql.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    port=int(os.getenv('MYSQL_PORT', 3306)),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
)

cursor = conn.cursor()

# Buat database
database_name = os.getenv('MYSQL_DATABASE', 'tgbot_verify')
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

print(f"✅ Database '{database_name}' berhasil dibuat!")

cursor.close()
conn.close()
