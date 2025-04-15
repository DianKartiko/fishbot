from database.db import delete_all_pengeluaran, delete_all_pendapatan
from telegram.ext import CallbackContext

def delete_all(update, context: CallbackContext):
    # Menghapus semua data pengeluaran dan pendapatan
    delete_all_pengeluaran()
    delete_all_pendapatan()
    
    update.message.reply_text("Semua data pengeluaran dan pendapatan telah dihapus. Anda dapat memasukkan data baru.")
