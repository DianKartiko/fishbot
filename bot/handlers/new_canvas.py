from telegram import Update
from telegram.ext import CallbackContext
from database.db import move_to_history

def new_canvas(update: Update, context: CallbackContext):
    move_to_history()  # Pindahkan data lama ke history
    update.message.reply_text("Canvas baru telah dimulai! Silakan masukkan data baru.")
