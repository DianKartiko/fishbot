from database.db import delete_all, delete_item
from telegram.ext import CallbackContext

def delete_all_data(update, context: CallbackContext):
    # Menghapus semua data pengeluaran dan pendapatan
    delete_all()
    update.message.reply_text("Semua data pengeluaran dan pendapatan telah dihapus. Anda dapat memasukkan data baru.")

def delete_data(update, context: CallbackContext):
    # Menghapus satu data berdasarkan id 
        # Contoh: /delete pengeluaran 5
    command_parts = update.message.text.split()
    
    if len(command_parts) != 3:
        update.message.reply_text("Format salah. Gunakan: /delete <pengeluaran/pendapatan> <id>")
        return
    
    table_name = command_parts[1]
    item_id = int(command_parts[2])
    
    if table_name not in ['pengeluaran', 'pendapatan']:
        update.message.reply_text("Tabel tidak valid. Pilih: pengeluaran/pendapatan")
        return
    
    success = delete_item(table_name, item_id)
    
    if success:
        update.message.reply_text(f"Data ID {item_id} di {table_name} berhasil dihapus 🗑️")
    else:
        update.message.reply_text("Gagal menghapus data. Cek ID atau koneksi database.")
