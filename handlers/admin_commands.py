"""Handler perintah admin"""
import asyncio
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command

logger = logging.getLogger(__name__)


async def addbalance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /addbalance - admin menambah poin"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cara pakai: /addbalance <user_id> <jumlah poin>\n\nContoh: /addbalance 123456789 10"
        )
        return

    try:
        target_user_id = int(context.args[0])
        amount = int(context.args[1])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("Pengguna tidak ditemukan.")
            return

        if db.add_balance(target_user_id, amount):
            user = db.get_user(target_user_id)
            await update.message.reply_text(
                f"✅ Berhasil menambah {amount} poin untuk pengguna {target_user_id}.\n"
                f"Saldo saat ini:{user['balance']}"
            )
        else:
            await update.message.reply_text("Operasi gagal, coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format argumen salah, masukkan angka yang valid.")


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /block - admin memasukkan pengguna ke daftar hitam"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cara pakai: /block <user_id>\n\nContoh: /block 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("Pengguna tidak ditemukan.")
            return

        if db.block_user(target_user_id):
            await update.message.reply_text(f"✅ Pengguna {target_user_id} sudah dimasukkan ke daftar hitam.")
        else:
            await update.message.reply_text("Operasi gagal, coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format argumen salah, masukkan user ID yang valid.")


async def white_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /white - admin menghapus pengguna dari daftar hitam"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cara pakai: /white <user_id>\n\nContoh: /white 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("Pengguna tidak ditemukan.")
            return

        if db.unblock_user(target_user_id):
            await update.message.reply_text(f"✅ Pengguna {target_user_id} sudah dikeluarkan dari daftar hitam.")
        else:
            await update.message.reply_text("Operasi gagal, coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format argumen salah, masukkan user ID yang valid.")


async def blacklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /blacklist - lihat daftar hitam"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    blacklist = db.get_blacklist()

    if not blacklist:
        await update.message.reply_text("Daftar hitam kosong.")
        return

    msg = "📋 Daftar pengguna yang diblokir:\n\n"
    for user in blacklist:
        msg += f"User ID: {user['user_id']}\n"
        msg += f"Username: @{user['username']}\n"
        msg += f"Nama: {user['full_name']}\n"
        msg += "---\n"

    await update.message.reply_text(msg)


async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /genkey - admin membuat kode"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cara pakai: /genkey <kode> <poin> [jumlah pakai] [masa aktif (hari)]\n\n"
            "Contoh:\n"
            "/genkey wandouyu 20 - membuat kode 20 poin (sekali pakai, tanpa kedaluwarsa)\n"
            "/genkey vip100 50 10 - membuat kode 50 poin (10 kali pakai, tanpa kedaluwarsa)\n"
            "/genkey temp 30 1 7 - membuat kode 30 poin (sekali pakai, kedaluwarsa 7 hari)"
        )
        return

    try:
        key_code = context.args[0].strip()
        balance = int(context.args[1])
        max_uses = int(context.args[2]) if len(context.args) > 2 else 1
        expire_days = int(context.args[3]) if len(context.args) > 3 else None

        if balance <= 0:
            await update.message.reply_text("Jumlah poin harus lebih besar dari 0.")
            return

        if max_uses <= 0:
            await update.message.reply_text("Jumlah pemakaian harus lebih besar dari 0.")
            return

        if db.create_card_key(key_code, balance, user_id, max_uses, expire_days):
            msg = (
                "✅ Kode berhasil dibuat!\n\n"
                f"Kode: {key_code}\n"
                f"Poin: {balance}\n"
                f"Jumlah pemakaian: {max_uses} kali\n"
            )
            if expire_days:
                msg += f"Masa berlaku: {expire_days} hari\n"
            else:
                msg += "Masa berlaku: permanen\n"
            msg += f"\nCara menggunakan: /use {key_code}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Kode sudah ada atau gagal dibuat, silakan gunakan nama lain.")
    except ValueError:
        await update.message.reply_text("Format argumen salah, masukkan angka yang valid.")


async def listkeys_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /listkeys - admin melihat daftar kode"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    keys = db.get_all_card_keys()

    if not keys:
        await update.message.reply_text("Belum ada kode.")
        return

    msg = "📋 Daftar kode:\n\n"
    for key in keys[:20]:  # menampilkan 20 entri pertama
        msg += f"Kode: {key['key_code']}\n"
        msg += f"Poin: {key['balance']}\n"
        msg += f"Jumlah pemakaian:{key['current_uses']}/{key['max_uses']}\n"

        if key["expire_at"]:
            expire_time = datetime.fromisoformat(key["expire_at"])
            if datetime.now() > expire_time:
                msg += "Status: kedaluwarsa\n"
            else:
                days_left = (expire_time - datetime.now()).days
                msg += f"Status: aktif (tersisa{days_left} hari)\n"
        else:
            msg += "Status: permanen\n"

        msg += "---\n"

    if len(keys) > 20:
        msg += f"\n(Menampilkan 20 entri pertama dari total {len(keys)})"

    await update.message.reply_text(msg)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani /broadcast - admin mengirim pesan massal"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    text = " ".join(context.args).strip() if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or ""

    if not text:
        await update.message.reply_text("Cara pakai: /broadcast <pesan>, atau balas sebuah pesan lalu kirim /broadcast")
        return

    user_ids = db.get_all_user_ids()
    success, failed = 0, 0

    status_msg = await update.message.reply_text(f"📢 Mulai menyiarkan ke {len(user_ids)}  pengguna...")

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
            success += 1
            await asyncio.sleep(0.05)  # Batasi kecepatan untuk menghindari limit
        except Exception as e:
            logger.warning("Gagal mengirim ke %s: %s", uid, e)
            failed += 1

    await status_msg.edit_text(f"✅ Selesai disiarkan!\nBerhasil: {success}\nGagal: {failed}")
