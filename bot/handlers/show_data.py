from telegram import Update
from telegram.ext import CallbackContext
from database.db import get_all_pengeluaran, get_all_pendapatan

def show_pengeluaran(update: Update, context: CallbackContext):
    data = get_all_pengeluaran()

    if not data:
        update.message.reply_text("Belum ada data pengeluaran.")
        return

    text = "📦 *Daftar Pengeluaran:*\n"
    for i, row in enumerate(data, 1):
        text += f"{i}. {row[1]} - Rp{row[2]} ({row[3]})\n"

    update.message.reply_text(text, parse_mode="Markdown")

def show_pendapatan(update: Update, context: CallbackContext):
    data = get_all_pendapatan()

    if not data:
        update.message.reply_text("Belum ada data pendapatan.")
        return

    text = "💰 *Daftar Pendapatan Panen:*\n"
    for i, row in enumerate(data, 1):
        text += f"{i}. {row[1]} - Rp{row[2]} ({row[3]})\n"

    update.message.reply_text(text, parse_mode="Markdown")


def show_data(update: Update, context: CallbackContext):
    pengeluaran_list = get_all_pengeluaran()
    pendapatan_list = get_all_pendapatan()

    message = "📦 *[Pengeluaran]*\n"
    if pengeluaran_list:
        for i, row in enumerate(pengeluaran_list, start=1):
            message += f"{i}. {row[1]} - Rp{row[2]:,} ({row[3]})\n"
    else:
        message += "Belum ada data pengeluaran.\n"

    message += "\n💰 *[Pendapatan Panen]*\n"
    if pendapatan_list:
        for i, row in enumerate(pendapatan_list, start=1):
            message += f"{i}. {row[1]} - Rp{row[2]:,} ({row[3]})\n"
    else:
        message += "Belum ada data pendapatan.\n"

    update.message.reply_text(message, parse_mode='Markdown')
    