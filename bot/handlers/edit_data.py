from telegram import Update
from telegram.ext import CallbackContext
from database.db import get_all_pengeluaran, update_pengeluaran, get_all_pendapatan, update_pendapatan
from telegram.ext import ConversationHandler

# Define states
SELECT_DATA, EDIT_ATTRIBUTE, EDIT_KETERANGAN, EDIT_HARGA, EDIT_TANGGAL = range(5)

def show_data(update: Update, context: CallbackContext):
    pengeluaran = get_all_pengeluaran()
    pendapatan = get_all_pendapatan()

    all_data = [("pengeluaran", item) for item in pengeluaran] + [("pendapatan", item) for item in pendapatan]

    if not all_data:
        update.message.reply_text("Tidak ada data untuk diedit.")
        return ConversationHandler.END

    text = "Pilih data yang ingin diedit:\n\n"
    for idx, (data_type, item) in enumerate(all_data):
        text += f"{idx + 1}. ({data_type.upper()}) {item[1]} - {item[2]} - {item[3]}\n"

    context.user_data["all_data"] = all_data
    update.message.reply_text(text)
    return SELECT_DATA

def select_data(update: Update, context: CallbackContext):
    try:
        choice = int(update.message.text) - 1
        all_data = context.user_data["all_data"]

        if choice < 0 or choice >= len(all_data):
            update.message.reply_text("Pilihan tidak valid, coba lagi.")
            return SELECT_DATA

        selected_type, selected_item = all_data[choice]
        context.user_data['selected_type'] = selected_type
        context.user_data['selected_data'] = selected_item

        update.message.reply_text(
            f"Anda memilih:\n{selected_item[1]} - {selected_item[2]} - {selected_item[3]}\n\n"
            "Pilih atribut yang ingin diedit:\n1. Keterangan\n2. Harga\n3. Tanggal"
        )
        return EDIT_ATTRIBUTE

    except ValueError:
        update.message.reply_text("Mohon masukkan angka yang valid.")
        return SELECT_DATA

def edit_attribute(update: Update, context: CallbackContext):
    choice = update.message.text.strip()

    if choice == "1":  # Keterangan
        update.message.reply_text("Masukkan keterangan baru:")
        return EDIT_KETERANGAN
    elif choice == "2":  # Harga
        update.message.reply_text("Masukkan harga baru:")
        return EDIT_HARGA
    elif choice == "3":  # Tanggal
        update.message.reply_text("Masukkan tanggal baru (YYYY-MM-DD):")
        return EDIT_TANGGAL
    else:
        update.message.reply_text("Pilihan tidak valid. Silakan pilih 1 (Keterangan), 2 (Harga), atau 3 (Tanggal).")
        return EDIT_ATTRIBUTE

def edit_keterangan(update: Update, context: CallbackContext):
    new_keterangan = update.message.text
    context.user_data['new_keterangan'] = new_keterangan
    update.message.reply_text("Masukkan harga baru:")
    return EDIT_HARGA

def edit_harga(update: Update, context: CallbackContext):
    try:
        new_harga = int(update.message.text)
        context.user_data['new_harga'] = new_harga
        update.message.reply_text("Masukkan tanggal baru (YYYY-MM-DD):")
        return EDIT_TANGGAL
    except ValueError:
        update.message.reply_text("Mohon masukkan harga dalam angka. Coba lagi.")
        return EDIT_HARGA

def edit_tanggal(update: Update, context: CallbackContext):
    new_tanggal = update.message.text
    selected_data = context.user_data.get('selected_data')
    selected_type = context.user_data.get('selected_type')

    if not selected_data or not selected_type:
        update.message.reply_text("Terjadi kesalahan. Mohon mulai dari awal dengan /edit.")
        return ConversationHandler.END

    new_keterangan = context.user_data.get('new_keterangan')
    new_harga = context.user_data.get('new_harga')

    if new_keterangan is None or new_harga is None:
        update.message.reply_text("Terjadi kesalahan. Mohon mulai dari awal dengan /edit.")
        return ConversationHandler.END

    if selected_type == "pengeluaran":
        update_pengeluaran(selected_data[0], new_keterangan, new_harga, new_tanggal)
    elif selected_type == "pendapatan":
        update_pendapatan(selected_data[0], new_keterangan, new_harga, new_tanggal)

    update.message.reply_text(
        f"Data berhasil diupdate:\nKeterangan: {new_keterangan}\nHarga: {new_harga}\nTanggal: {new_tanggal}"
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Proses edit data dibatalkan.")
    return ConversationHandler.END
