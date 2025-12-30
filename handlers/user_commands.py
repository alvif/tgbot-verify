"""Handler perintah pengguna"""
import logging
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command
from utils.messages import (
    get_welcome_message,
    get_about_message,
    get_help_message,
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /start"""
    if await reject_group_command(update):
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    full_name = user.full_name or ""

    # Jika sudah diinisialisasi langsung keluar
    if db.user_exists(user_id):
        await update.message.reply_text(
            f"Selamat datang kembali, {full_name}!\n"
            "Anda sudah menyelesaikan inisialisasi.\n"
            "Kirim /help untuk melihat perintah yang tersedia."
        )
        return

    # Bagikan undangan
    invited_by: Optional[int] = None
    if context.args:
        try:
            invited_by = int(context.args[0])
            if not db.user_exists(invited_by):
                invited_by = None
        except Exception:
            invited_by = None

    # Buat pengguna
    if db.create_user(user_id, username, full_name, invited_by):
        welcome_msg = get_welcome_message(full_name, bool(invited_by))
        await update.message.reply_text(welcome_msg)
    else:
        await update.message.reply_text("Pendaftaran gagal, coba lagi nanti.")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /about"""
    if await reject_group_command(update):
        return

    await update.message.reply_text(get_about_message())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /help"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    is_admin = user_id == ADMIN_USER_ID
    await update.message.reply_text(get_help_message(is_admin))


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /balance"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda masuk daftar hitam dan tidak bisa memakai fitur ini.")
        return

    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("Silakan gunakan /start untuk mendaftar terlebih dahulu.")
        return

    await update.message.reply_text(
        f"💰 Saldo poin\n\nJumlah saat ini: {user['balance']} poin"
    )


async def checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /qd untuk check-in - sementara dinonaktifkan"""
    user_id = update.effective_user.id

    # Fitur check-in sementara dimatikan (memperbaiki bug)
    # await update.message.reply_text(
    #     "⚠️ Fitur check-in sedang dalam perawatan\n\n"
    #     "Kami menemukan bug sehingga fitur ini sementara dimatikan.\n"
    #     "Akan segera aktif kembali, mohon maaf atas ketidaknyamanan ini.\n\n"
    #     "💡 Anda masih dapat memperoleh poin lewat:\n"
    #     "• Undang teman dengan /invite (+2 poin)\n"
    #     "• Tukarkan kode dengan /use <kode>"
    # )
    # return
    
    # ===== Kode di bawah ini dinonaktifkan =====
    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda masuk daftar hitam dan tidak bisa memakai fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk mendaftar terlebih dahulu.")
        return

    # Langkah validasi pertama: lakukan di level handler
    if not db.can_checkin(user_id):
        await update.message.reply_text("❌ Anda sudah check-in hari ini, silakan kembali besok.")
        return

    # Langkah validasi kedua: lakukan di level database (operasi atomik SQL)
    if db.checkin(user_id):
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"✅ Check-in berhasil!\nPoin didapat: +1\nSaldo sekarang: {user['balance']} poin"
        )
    else:
        # Jika database mengembalikan False artinya sudah check-in hari ini (lapisan ganda)
        await update.message.reply_text("❌ Anda sudah check-in hari ini, silakan kembali besok.")


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /invite"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda masuk daftar hitam dan tidak bisa memakai fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk mendaftar terlebih dahulu.")
        return

    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🎁 Tautan undangan khusus Anda:\n{invite_link}\n\n"
        "Setiap pengguna yang bergabung melalui tautan ini memberi Anda 2 poin."
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Tangani perintah /use untuk menukar kode"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda masuk daftar hitam dan tidak bisa memakai fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk mendaftar terlebih dahulu.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cara pakai: /use <kode>\n\nContoh: /use wandouyu"
        )
        return

    key_code = context.args[0].strip()
    result = db.use_card_key(key_code, user_id)

    if result is None:
        await update.message.reply_text("Kode tidak ditemukan, mohon periksa lalu coba lagi.")
    elif result == -1:
        await update.message.reply_text("Kode tersebut sudah mencapai batas pemakaian.")
    elif result == -2:
        await update.message.reply_text("Kode tersebut sudah kedaluwarsa.")
    elif result == -3:
        await update.message.reply_text("Anda sudah pernah memakai kode tersebut.")
    else:
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"Kode berhasil digunakan!\nPoin diterima: {result}\nSaldo sekarang: {user['balance']}"
        )
