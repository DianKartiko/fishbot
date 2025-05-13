from telegram import Update
from telegram.ext import CallbackContext

# Handler /start
def start_bot(update: Update, context: CallbackContext):
    print("Start command received!")
    update.message.reply_text("Selamat datang di Bot Keuangan Ikan Maskoki! 🐟")