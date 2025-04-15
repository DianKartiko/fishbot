from telegram import Update
from telegram.ext import CallbackContext
from database.db import get_all_pengeluaran, get_all_pendapatan

def total_keuangan(update: Update, context: CallbackContext):
    pengeluaran_list = get_all_pengeluaran()
    pendapatan_list = get_all_pendapatan()

    total_pengeluaran = sum([row[2] for row in pengeluaran_list])
    total_pendapatan = sum([row[2] for row in pendapatan_list])

    keuangan_message = f"💸 Total Pengeluaran: Rp{total_pengeluaran:,}\n"
    keuangan_message += f"💰 Total Pendapatan: Rp{total_pendapatan:,}\n"
    keuangan_message += f"💡 Selisih (Pendapatan - Pengeluaran): Rp{total_pendapatan - total_pengeluaran:,}"

    if total_pengeluaran > total_pendapatan:
        keuangan_message += "\n\n🚨 Anda mengalami kerugian!"
    elif total_pengeluaran < total_pendapatan:
        keuangan_message += "\n\n✅ Anda mendapatkan keuntungan!"
    else:     
        keuangan_message += "\n\n⚖️ Keuangan Anda seimbang!"

    update.message.reply_text(keuangan_message)
