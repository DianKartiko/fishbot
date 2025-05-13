from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler,MessageHandler, Filters, CommandHandler
from database.db import save_pendapatan

# Tahapan input
KETERANGAN, TOTAL, TANGGAL = range(3)

# Memulai input pendapatan
def start_input_pendapatan(update: Update, context: CallbackContext):
    update.message.reply_text("Silakan kirim keterangan panen (misalnya: Panen April).")
    return KETERANGAN

# Menerima keterangan
def receive_keterangan(update: Update, context: CallbackContext):
    context.user_data['keterangan'] = update.message.text
    update.message.reply_text("Sekarang kirim total pendapatan (angka).")
    return TOTAL

# Menerima total
def receive_total(update: Update, context: CallbackContext):
    try:
        total = int(update.message.text)
        context.user_data['total'] = total
        update.message.reply_text("Terakhir, kirim tanggal panen (YYYY-MM-DD).")
        return TANGGAL
    except ValueError:
        update.message.reply_text("Mohon masukkan angka yang valid untuk total pendapatan.")
        return TOTAL

# Menerima tanggal dan simpan data
def receive_tanggal(update: Update, context: CallbackContext):
    tanggal = update.message.text

    keterangan = context.user_data['keterangan']
    total = context.user_data['total']
    context.user_data['tanggal'] = tanggal

    # Simpan ke database
    save_pendapatan(keterangan, total, tanggal)

    update.message.reply_text(
        f"✅ Data pendapatan disimpan:\n"
        f"Keterangan: {keterangan}\n"
        f"Total: Rp{total}\n"
        f"Tanggal: {tanggal}"
    )
    return ConversationHandler.END

# Cancel
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Input pendapatan dibatalkan.")
    return ConversationHandler.END

# Handler untuk pendapatan 
conv_handler_pendapatan = ConversationHandler(
    entry_points=[CommandHandler('input_pendapatan', start_input_pendapatan)],
    states={
        KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, receive_keterangan)],
        TOTAL: [MessageHandler(Filters.text & ~Filters.command, receive_total)],
        TANGGAL: [MessageHandler(Filters.text & ~Filters.command, receive_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)