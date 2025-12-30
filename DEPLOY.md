# Panduan Deployment Bot SheerID

Dokumen ini menjelaskan cara menjalankan bot verifikasi SheerID pada berbagai lingkungan.

## 1. Persyaratan Lingkungan

| Kategori | Minimum | Rekomendasi |
|----------|---------|-------------|
| Sistem Operasi | Linux/Windows/macOS | Ubuntu 22.04 LTS |
| Python | 3.11 | 3.11 |
| MySQL | 5.7 | 8.0 |
| RAM | 512 MB | 2 GB |
| Penyimpanan | 2 GB | 5 GB |
| Koneksi | Internet stabil | 10 Mbps |

## 2. Deployment Singkat

1. Kloning repositori dan buat file `.env` dari `env.example`.
2. Jalankan `pip install -r requirements.txt` lalu `playwright install chromium`.
3. Atur variabel lingkungan pada `.env`.
4. Jalankan `python bot.py` untuk mode pengujian.
5. Gunakan `screen`, `tmux`, atau systemd untuk menjalankan secara daemon.

## 3. Deployment dengan Docker

### 3.1 Menggunakan Docker Compose
1. Buat `.env` (lihat contoh di atas).
2. Jalankan `docker compose up -d`.
3. Cek status dengan `docker compose ps` atau `docker compose logs -f bot`.
4. Untuk memperbarui kode jalankan `git pull` kemudian `docker compose up -d --build`.

### 3.2 Manual (docker run)
1. `docker build -t sheerid-bot .`
2. `docker run --name sheerid-bot --env-file .env -d sheerid-bot`
3. Gunakan `docker logs -f sheerid-bot` untuk memantau.

## 4. Deployment Manual Tanpa Docker

1. Pasang Python, pip, dan MySQL sesuai OS.
2. Buat virtual environment (`python -m venv .venv`).
3. `source .venv/bin/activate` (Linux/macOS) atau `.\.venv\Scripts\activate` (Windows).
4. `pip install -r requirements.txt` kemudian `playwright install chromium`.
5. Konfigurasi database, buat user khusus, dan isi `.env`.
6. Jalankan `python bot.py` atau gunakan `nohup python bot.py &` untuk background.

## 5. Variabel Lingkungan

```
BOT_TOKEN=
CHANNEL_USERNAME=
CHANNEL_URL=
ADMIN_USER_ID=
MYSQL_HOST=
MYSQL_PORT=3306
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DATABASE=
```

Sesuaikan nilai ini pada `.env`. Pastikan akun MySQL memiliki izin CREATE/INSERT/UPDATE.

## 6. Konfigurasi Poin

Ubah `config.py` sesuai kebutuhan:
```
VERIFY_COST = 1
CHECKIN_REWARD = 1
INVITE_REWARD = 2
REGISTER_REWARD = 1
```

## 7. FAQ Singkat

1. **Token bot tidak valid** – Periksa `.env` dan pastikan nilai dari @BotFather benar.
2. **Tidak bisa konek MySQL** – Pastikan MySQL berjalan, kredensial benar, dan firewall membuka port 3306.
3. **Playwright error** – Jalankan `playwright install chromium` pada lingkungan yang sama dengan bot.
4. **Port sudah dipakai** – Atur ulang port pada `docker-compose.yml` atau hentikan layanan lain.
5. **Memori tidak cukup** – Kurangi konkurensi pada `utils/concurrency.py` atau tambahkan RAM.

## 8. Pemeliharaan

- **Log**: `docker compose logs -f bot` atau lihat file log pada folder `logs/`.
- **Backup DB**: `mysqldump -u user -p dbname > backup.sql`.
- **Update kode**: `git pull` kemudian restart bot.
- **Systemd**: buat file `/etc/systemd/system/tgbot-verify.service` untuk menjalankan sebagai layanan.
- **Supervisor**: siapkan file `tgbot-verify.conf` jika lebih nyaman menggunakan supervisor.

## 9. Keamanan

1. Gunakan password kuat untuk bot dan database.
2. Batasi akses MySQL hanya dari host yang perlu.
3. Terapkan firewall (buka port 22/80/443 sesuai kebutuhan).
4. Rutin memperbarui sistem dan dependensi.
5. Jangan commit `.env` atau kredensial lain.

## 10. Bantuan

- Channel Telegram: https://t.me/pk_oa
- Laporan bug: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

Semoga deployment berjalan lancar!
