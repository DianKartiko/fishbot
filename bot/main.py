from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from bot.handlers import pengeluaran
from bot.handlers import pendapatan
from bot.handlers import show_data
from bot.handlers import edit_data
from bot.handlers import total
from bot.handlers import report, delete_data, new_canvas
from database.db import create_tables
import os

# Ganti dengan token asli kamu
BOT_TOKEN = "7859479447:AAF7HAv91DcdIWZQOtiFQY8ovW-ZvSqz_Ck"

create_tables()  # Pastikan tabel sudah dibuat sebelum bot berjalan

def start(update, context):
    update.message.reply_text("Selamat datang di Bot Keuangan Ikan Maskoki! 🐟")

def start_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Conversation handler untuk pengeluaran
    conv_handler_pengeluaran = ConversationHandler(
        entry_points=[CommandHandler('input_pengeluaran', pengeluaran.start_input_pengeluaran)],
        states={
            pengeluaran.KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_keterangan)],
            pengeluaran.HARGA: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_harga)],
            pengeluaran.TANGGAL: [MessageHandler(Filters.text & ~Filters.command, pengeluaran.receive_tanggal)],
        },
        fallbacks=[CommandHandler('cancel', pengeluaran.cancel)],
    )
    dp.add_handler(conv_handler_pengeluaran)

    # Conversation handler untuk pendapatan
    conv_handler_pendapatan = ConversationHandler(
        entry_points=[CommandHandler('input_pendapatan', pendapatan.start_input_pendapatan)],
        states={
            pendapatan.KETERANGAN: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_keterangan)],
            pendapatan.TOTAL: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_total)],
            pendapatan.TANGGAL: [MessageHandler(Filters.text & ~Filters.command, pendapatan.receive_tanggal)],
        },
        fallbacks=[CommandHandler('cancel', pendapatan.cancel)],
    )
    dp.add_handler(conv_handler_pendapatan)

    # Conversation handler untuk edit data
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
    dp.add_handler(conv_handler_edit_data)

    dp.add_handler(CommandHandler("show_pengeluaran", show_data.show_pengeluaran))
    dp.add_handler(CommandHandler("show_pendapatan", show_data.show_pendapatan))
    dp.add_handler(CommandHandler("show_data", show_data.show_data))

    # Total Keuangan
    dp.add_handler(CommandHandler("total_keuangan", total.total_keuangan))

    # New Canvas, Report, and delete_all_data
    dp.add_handler(CommandHandler("new_canvas", new_canvas.new_canvas))
    dp.add_handler(CommandHandler("report", report.report))
    dp.add_handler(CommandHandler("delete_all", delete_data.delete_all))

    updater.start_polling()
    updater.idle()

# Memulai bot
start_bot()
