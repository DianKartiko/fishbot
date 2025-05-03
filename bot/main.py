from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from bot.handlers import pengeluaran, pendapatan, show_data, edit_data, total, report, delete_data, new_canvas
from database.db import create_tables
from config import BOT_TOKEN
import os

create_tables()

app = Flask(__name__)
bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# Handler /start
def start_bot(update: Update, context: CallbackContext):
    update.message.reply_text("Selamat datang di Bot Keuangan Ikan Maskoki! 🐟")

dispatcher.add_handler(CommandHandler("start", start_bot))

# === Pengeluaran ===
conv_handler_pengeluaran = ConversationHandler(
    entry_points=[CommandHandler('input_pengeluaran', pengeluaran.start_input_pengeluaran)],
    states={
        pengeluaran.KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_keterangan)],
        pengeluaran.HARGA: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_harga)],
        pengeluaran.TANGGAL: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', pengeluaran.cancel)],
)
dispatcher.add_handler(conv_handler_pengeluaran)

# === Pendapatan ===
conv_handler_pendapatan = ConversationHandler(
    entry_points=[CommandHandler('input_pendapatan', pendapatan.start_input_pendapatan)],
    states={
        pendapatan.KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_keterangan)],
        pendapatan.TOTAL: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_total)],
        pendapatan.TANGGAL: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', pendapatan.cancel)],
)
dispatcher.add_handler(conv_handler_pendapatan)

# === Edit Data ===
conv_handler_edit_data = ConversationHandler(
    entry_points=[CommandHandler('edit_data', edit_data.show_data)],
    states={
        edit_data.SELECT_DATA: [MessageHandler(Filters.text & ~Filters.command, edit_data.select_data)],
        edit_data.EDIT_ATTRIBUTE: [MessageHandler(Filters.text & ~Filters.command, edit_data.edit_attribute)],
        edit_data.EDIT_KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, edit_data.edit_keterangan)],
        edit_data.EDIT_HARGA: [MessageHandler(Filters.text & ~Filters.command, edit_data.edit_harga)],
        edit_data.EDIT_TANGGAL: [MessageHandler(Filters.text & ~Filters.command, edit_data.edit_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', edit_data.cancel)],
)
dispatcher.add_handler(conv_handler_edit_data)

# === Command lainnya ===
dispatcher.add_handler(CommandHandler("show_pengeluaran", show_data.show_pengeluaran))
dispatcher.add_handler(CommandHandler("show_pendapatan", show_data.show_pendapatan))
dispatcher.add_handler(CommandHandler("show_data", show_data.show_data))
dispatcher.add_handler(CommandHandler("total_keuangan", total.total_keuangan))
dispatcher.add_handler(CommandHandler("new_canvas", new_canvas.new_canvas))
dispatcher.add_handler(CommandHandler("report", report.report))
dispatcher.add_handler(CommandHandler("delete_all", delete_data.delete_all))


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """Endpoint untuk menerima update dari Telegram"""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # Hapus webhook lama (opsional, untuk memastikan)
    bot.delete_webhook()
    
    # Set webhook baru
    URL = os.environ.get("URL", "https://fishbot.fly.dev")
    webhook_url = f"{URL}/{BOT_TOKEN}"
    print(f"🔄 Setting webhook to: {webhook_url}")  # Debugging
    bot.set_webhook(webhook_url)
    
    # Jalankan Flask
    port = int(os.environ.get("PORT", 8080))  # Fly.io default: 8080
    app.run(host="0.0.0.0", port=port)