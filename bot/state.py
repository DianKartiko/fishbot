from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from bot.handlers import pengeluaran, pendapatan, show_data, edit_data, total, report, delete_data, new_canvas
from database.db import create_tables
import os 

# Creating Tables from Database

create_tables()

# Getting API_KEY from telegram bots
API_KEY = os.getenv("API_KEY")

# dp 
dp = Dispatcher(API_KEY, None, use_context=True)

# Handler /start
def start_bot(update: Update, context: CallbackContext):
    update.message.reply_text("Selamat datang di Bot Keuangan Ikan Maskoki! 🐟")

# Handler untuk pengeluaran
conv_handler_pengeluaran = ConversationHandler(
    entry_points=[CommandHandler('input_pengeluaran', pengeluaran.start_input_pengeluaran)],
    states={
        pengeluaran.KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_keterangan)],
        pengeluaran.HARGA: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_harga)],
        pengeluaran.TANGGAL: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', pengeluaran.cancel)],
)

# Handler untuk pendapatan 
conv_handler_pendapatan = ConversationHandler(
    entry_points=[CommandHandler('input_pendapatan', pendapatan.start_input_pendapatan)],
    states={
        pendapatan.KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_keterangan)],
        pendapatan.TOTAL: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_total)],
        pendapatan.TANGGAL: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_tanggal)],
    },
    fallbacks=[CommandHandler('cancel', pendapatan.cancel)],
)

# Editing Data Untuk Data yang salah
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

# ==== Command Handler ====
dp.add_handler(CommandHandler("start", start_bot)) # Untuk memulai chat / start
dp.add_handler(conv_handler_pengeluaran) # Untuk memulai handler pengeluaran / Input Pengeluaran
dp.add_handler(conv_handler_pendapatan) # Untuk memulai handler pendapatan / Input pendapatan 
dp.add_handler(conv_handler_edit_data) # Untuk memulai handler edit data / editing data 
dp.add_handler(CommandHandler("show_pengeluaran", show_data.show_pengeluaran)) # Untuk Show Data Pengeluaran
dp.add_handler(CommandHandler("show_pendapatan", show_data.show_pendapatan)) # Untuk Show Data Pendapatan
dp.add_handler(CommandHandler("show_data", show_data.show_data)) # Untuk Show data Keseluruhan
dp.add_handler(CommandHandler("total_keuangan", total.total_keuangan)) # Untuk Melihat Total Keuangan 
dp.add_handler(CommandHandler("new_canvas", new_canvas.new_canvas)) # Untuk Memulai Canvas yang baru
dp.add_handler(CommandHandler("report", report.report)) # Untuk membuat Report 
dp.add_handler(CommandHandler("delete_all", delete_data.delete_all)) # Menghapus Seluruh Data