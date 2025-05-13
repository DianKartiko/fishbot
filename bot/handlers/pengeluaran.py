# bot/handlers/pengeluaran.py
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler,  MessageHandler, Filters, CommandHandler
from database.db import save_pengeluaran

# Define stages
KETERANGAN, HARGA, TANGGAL = range(3)

# Start conversation
def start_input_pengeluaran(update: Update, context: CallbackContext):
    update.message.reply_text("Silakan kirim keterangan barang yang dibeli.")
    return KETERANGAN

# Receive Keterangan
def receive_keterangan(update: Update, context: CallbackContext):
    context.user_data['keterangan'] = update.message.text
    update.message.reply_text("Sekarang kirim harga barang.")
    return HARGA

# Receive Harga
def receive_harga(update: Update, context: CallbackContext):
    try:
        harga = int(update.message.text)
        context.user_data['harga'] = harga
        update.message.reply_text("Terakhir, kirim tanggal pembelian (YYYY-MM-DD).")
        return TANGGAL
    except ValueError:
        update.message.reply_text("Mohon masukkan harga dalam angka. Coba lagi.")
        return HARGA

# Receive Tanggal
def receive_tanggal(update: Update, context: CallbackContext):
    tanggal = update.message.text
    context.user_data['tanggal'] = tanggal

    # Save to database
    keterangan = context.user_data['keterangan']
    harga = context.user_data['harga']
    tanggal = context.user_data['tanggal']
    
    save_pengeluaran(keterangan, harga, tanggal)

    update.message.reply_text(f"Data pengeluaran disimpan:\nKeterangan: {keterangan}\nHarga: {harga}\nTanggal: {tanggal}")
    return ConversationHandler.END

# Cancel conversation
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Pencatatan pengeluaran dibatalkan.")
    return ConversationHandler.END


conv_handler_pengeluaran = ConversationHandler(
    entry_points=[CommandHandler('input_pengeluaran', start_input_pengeluaran)],
    states={
        KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, receive_keterangan)],
        HARGA: [MessageHandler(Filters.text & ~Filters.command, receive_harga)],
        TANGGAL: [MessageHandler(Filters.text & ~Filters.command, receive_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)


