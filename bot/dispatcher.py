from telegram.ext import CommandHandler
from queue import Queue
from .handlers import ( 
    conv_handler_pengeluaran,
    conv_handler_pendapatan,
    conv_handler_edit_data,
    start_bot,
    show_pengeluaran,
    show_pendapatan,
    show_data,
    total_keuangan,
    new_canvas,
    report,
    delete_all_data,
    delete_data
) 
# Function Dispatcher
def setup_dispatcher(dp):
    # Seluruh handler dan Dispatcher
    dp.add_handler(CommandHandler("start", start_bot)) # Untuk memulai chat / start
    dp.add_handler(conv_handler_pengeluaran) # Untuk memulai handler pengeluaran / Input Pengeluaran
    dp.add_handler(conv_handler_pendapatan) # Untuk memulai handler pendapatan / Input pendapatan 
    dp.add_handler(conv_handler_edit_data) # Untuk memulai handler edit data / editing data 
    dp.add_handler(CommandHandler("show_pengeluaran", show_pengeluaran)) # Untuk Show Data Pengeluaran
    dp.add_handler(CommandHandler("show_pendapatan", show_pendapatan)) # Untuk Show Data Pendapatan
    dp.add_handler(CommandHandler("show_data", show_data)) # Untuk Show data Keseluruhan
    dp.add_handler(CommandHandler("total_keuangan", total_keuangan)) # Untuk Melihat Total Keuangan 
    dp.add_handler(CommandHandler("new_canvas", new_canvas)) # Untuk Memulai Canvas yang baru
    dp.add_handler(CommandHandler("report", report)) # Untuk membuat Report 
    dp.add_handler(CommandHandler("delete_all", delete_all_data)) # Menghapus Seluruh Data
    dp.add_handler(CommandHandler('delete_data', delete_data))