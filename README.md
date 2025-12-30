# Bot Telegram Verifikasi SheerID Otomatis

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> Bot Telegram yang membantu menyelesaikan verifikasi SheerID mahasiswa maupun guru secara otomatis.
> Dikembangkan dari basis kode [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) dengan banyak perbaikan.

---

## Gambaran Umum

Bot ini ditulis dengan Python. Ia membuat identitas fiktif, merender dokumen (PDF/PNG), lalu mengunggahnya ke platform SheerID sehingga proses verifikasi dapat selesai tanpa interaksi manual.

> **Penting:**
> - Modul **Gemini One Pro**, **ChatGPT Teacher K12**, **Spotify Student**, **YouTube Premium Student**, dan **Bolt.new Teacher** memerlukan `programId` terbaru. Pastikan memperbaruinya sebelum menjalankan bot.
> - Dokumentasi alur **verifikasi militer ChatGPT** tersedia pada [`military/README.md`](military/README.md) bila Anda ingin menambahkan layanan tersebut.

### Layanan yang Didukung

| Perintah | Layanan | Jenis | Status | Keterangan |
|---------|---------|------|--------|-----------|
| `/verify` | Gemini One Pro | Guru | Stabil | Diskon Google AI Studio |
| `/verify2` | ChatGPT Teacher K12 | Guru | Stabil | Diskon OpenAI ChatGPT |
| `/verify3` | Spotify Student | Mahasiswa | Stabil | Diskon langganan Spotify |
| `/verify4` | Bolt.new Teacher | Guru | Stabil | Diskon Bolt.new (kode otomatis) |
| `/verify5` | YouTube Premium Student | Mahasiswa | Beta | Diskon YouTube Premium |

YouTube memiliki format tautan berbeda sehingga Anda perlu mengambil `programId` dan `verificationId` sendiri (lihat `youtube/HELP.MD`).

### Fitur Utama

- Otomasi penuh (pembuatan identitas, dokumen, pengunggahan)
- Sistem poin dengan check-in, undangan, dan kode tukar
- Konkurensi cerdas dengan pembatasan per layanan
- Penyimpanan data di MySQL
- Dukungan broadcast admin dan blacklist

## Tumpukan Teknologi

- Python 3.11+
- python-telegram-bot 20+
- MySQL 5.7+
- Playwright Chromium
- httpx, Pillow, reportlab, xhtml2pdf
- python-dotenv

## Mulai Cepat

1. **Kloning repositori**
   ```bash
   git clone https://github.com/PastKing/tgbot-verify.git
   cd tgbot-verify
   ```
2. **Pasang dependensi**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. **Salin konfigurasi**
   ```bash
   cp env.example .env
   # Isi token bot, kredensial MySQL, URL channel, dsb.
   ```
4. **Jalankan bot**
   ```bash
   python bot.py
   ```

## Konfigurasi Lingkungan

```
# Telegram
BOT_TOKEN=
CHANNEL_USERNAME=
CHANNEL_URL=
ADMIN_USER_ID=

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DATABASE=
```

### Pengaturan Poin

Atur nilai pada `config.py` jika diperlukan:

```python
VERIFY_COST = 1
CHECKIN_REWARD = 1
INVITE_REWARD = 2
REGISTER_REWARD = 1
```

## Catatan Penting

- Perbarui `programId` untuk layanan yang Anda gunakan (lihat `one/config.py`, `k12/config.py`, `spotify/config.py`, `youtube/config.py`, `Boltnew/config.py`).
- Gunakan `.env` untuk menyimpan kredensial. Jangan commit nilai sensitif.
- Jalankan `playwright install chromium` pada lingkungan produksi (termasuk dalam Dockerfile bawaan).

## Tautan Berguna

- Channel Telegram: https://t.me/pk_oa
- Pelaporan masalah: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)
- Panduan deployment: [DEPLOY.md](DEPLOY.md)

## Pengembangan Lanjutan

1. Pertahankan atribusi penulis asli ketika melakukan fork.
2. Gunakan lisensi MIT yang sama untuk turunan proyek.
3. Penggunaan komersial menjadi tanggung jawab Anda sendiri; tidak ada dukungan resmi.

## Lisensi

Proyek ini berada di bawah [MIT License](LICENSE).

## Penghargaan

- Terima kasih kepada [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) sebagai inspirasi awal.
- Terima kasih kepada para kontributor dan platform SheerID.

## Changelog Singkat

- **v2.0.0** – Menambahkan Spotify & YouTube, meningkatkan konkurensi, memperbarui dokumentasi.
- **v1.0.0** – Rilis awal dengan dukungan Gemini, ChatGPT, dan Bolt.new.

Selamat menggunakan bot ini! Beri bintang bila Anda merasa terbantu.
