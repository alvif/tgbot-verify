"""Template pesan untuk berbagai command."""

from config import CHANNEL_URL, VERIFY_COST, HELP_NOTION_URL


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """Bangun pesan sambutan."""
    msg = (
        f"🎉 Selamat datang, {full_name}!\n"
        "Registrasi berhasil dan Anda menerima 1 poin.\n"
    )
    if invited_by:
        msg += "Terima kasih bergabung melalui tautan undangan, pengundang mendapatkan 2 poin.\n"

    msg += (
        "\nBot ini membantu menyelesaikan verifikasi SheerID secara otomatis.\n"
        "Mulai cepat:\n"
        "/about - kenali fungsi bot\n"
        "/balance - lihat saldo poin\n"
        "/help - daftar perintah lengkap\n\n"
        "Cara memperoleh poin tambahan:\n"
        "/qd - check-in harian\n"
        "/invite - undang teman\n"
        f"Bergabunglah dengan channel kami: {CHANNEL_URL}"
    )
    return msg


def get_about_message() -> str:
    """Bangun pesan tentang bot."""
    return (
        "🤖 Bot verifikasi otomatis SheerID\n\n"
        "Fitur:\n"
        "- Menyelesaikan verifikasi mahasiswa/guru SheerID secara otomatis\n"
        "- Mendukung Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, dan Bolt.new Teacher\n\n"
        "Cara mendapatkan poin:\n"
        "- Registrasi pertama mendapat 1 poin\n"
        "- Check-in harian +1 poin\n"
        "- Undang teman +2 poin per orang\n"
        "- Tukarkan kode sesuai ketentuan\n"
        f"- Ikuti channel kami: {CHANNEL_URL}\n\n"
        "Langkah penggunaan:\n"
        "1. Mulai proses verifikasi di situs resmi lalu salin tautannya\n"
        "2. Kirim perintah /verify, /verify2, /verify3, /verify4, atau /verify5 beserta tautan tersebut\n"
        "3. Tunggu hasil proses\n"
        "4. Untuk Bolt.new, kode akan diambil otomatis; gunakan /getV4Code <verification_id> bila butuh cek manual\n\n"
        "Gunakan /help untuk daftar perintah lengkap."
    )


def get_help_message(is_admin: bool = False) -> str:
    """Bangun pesan bantuan."""
    msg = (
        "📖 Bantuan bot verifikasi SheerID otomatis\n\n"
        "Perintah pengguna:\n"
        "/start - mulai dan registrasi\n"
        "/about - deskripsi bot\n"
        "/balance - lihat saldo poin\n"
        "/qd - check-in harian (+1 poin)\n"
        "/invite - buat tautan undangan (+2 poin/orang)\n"
        "/use <kode> - tukarkan kode untuk poin\n"
        f"/verify <tautan> - verifikasi Gemini One Pro (-{VERIFY_COST} poin)\n"
        f"/verify2 <tautan> - verifikasi ChatGPT Teacher K12 (-{VERIFY_COST} poin)\n"
        f"/verify3 <tautan> - verifikasi Spotify Student (-{VERIFY_COST} poin)\n"
        f"/verify4 <tautan> - verifikasi Bolt.new Teacher (-{VERIFY_COST} poin)\n"
        f"/verify5 <tautan> - verifikasi YouTube Student Premium (-{VERIFY_COST} poin)\n"
        "/getV4Code <verification_id> - ambil kode verifikasi Bolt.new\n"
        "/help - tampilkan pesan ini\n"
        f"Panduan kegagalan: {HELP_NOTION_URL}\n"
    )

    if is_admin:
        msg += (
            "\nPerintah admin:\n"
            "/addbalance <user_id> <poin> - tambah poin\n"
            "/block <user_id> - blokir pengguna\n"
            "/white <user_id> - hapus blokir\n"
            "/blacklist - lihat daftar blokir\n"
            "/genkey <kode> <poin> [jumlah] [hari] - buat kode\n"
            "/listkeys - daftar kode terakhir\n"
            "/broadcast <pesan> - kirim siaran ke semua pengguna\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """Bangun pesan saat poin tidak mencukupi."""
    return (
        f"Poin Anda tidak cukup! Diperlukan {VERIFY_COST} poin, saldo saat ini {current_balance} poin.\n\n"
        "Cara mendapatkan poin:\n"
        "- /qd untuk check-in harian\n"
        "- /invite untuk mengundang teman\n"
        "- /use <kode> untuk menukarkan kode\n"
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """Bangun instruksi penggunaan perintah verifikasi."""
    return (
        f"Cara pakai: {command} <tautan SheerID>\n\n"
        "Contoh:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "Cara mengambil tautan verifikasi:\n"
        f"1. Buka halaman verifikasi {service_name}\n"
        "2. Mulai proses verifikasi\n"
        "3. Salin URL lengkap dari browser\n"
        f"4. Kirim menggunakan perintah {command}"
    )
