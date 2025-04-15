import io
import os
from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
from database.db import get_all_pengeluaran, get_all_pengeluaran_history, get_all_pendapatan, get_all_pendapatan_history

def plot_data(labels, values, title="Grafik"):
    fig, ax = plt.subplots(figsize=(8, 5))

    if len(values) > 2:
        ax.plot(labels, values, marker='o', linestyle='-', color='blue')
        ax.set_title(f"{title} (Line Chart)")
    else:
        ax.bar(labels, values, color='green')
        ax.set_title(f"{title} (Bar Chart)")

    ax.set_xlabel("Kategori")
    ax.set_ylabel("Nilai")
    ax.grid(True, linestyle='--', alpha=0.5)

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)

    return buffer

def generate_report():
    pengeluaran = get_all_pengeluaran()
    pengeluaran_history = get_all_pengeluaran_history()
    pendapatan = get_all_pendapatan()
    pendapatan_history = get_all_pendapatan_history()

    # Buat folder 'reports' jika belum ada
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)

    # Nama file berdasarkan timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"laporan_keuangan_{timestamp}.pdf"
    pdf_path = os.path.join(reports_dir, pdf_filename)

    # Membuat PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Laporan Keuangan Ikan Maskoki", styles['Title']))
    elements.append(Spacer(1, 12))

    # Tabel Pengeluaran Terbaru
    if pengeluaran:
        elements.append(Paragraph("Pengeluaran Terbaru:", styles['Heading2']))
        data = [['Keterangan', 'Harga', 'Tanggal']]
        for item in pengeluaran:
            data.append([item[1], f"Rp{item[2]:,}", item[3]])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Tabel Pengeluaran Lama
    if pengeluaran_history:
        elements.append(Paragraph("Pengeluaran Lama (History):", styles['Heading2']))
        data = [['Keterangan', 'Harga', 'Tanggal']]
        for item in pengeluaran_history:
            data.append([item[1], f"Rp{item[2]:,}", item[3]])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Tabel Pendapatan Terbaru
    if pendapatan:
        elements.append(Paragraph("Pendapatan Terbaru:", styles['Heading2']))
        data = [['Keterangan', 'Total', 'Tanggal']]
        for item in pendapatan:
            data.append([item[1], f"Rp{item[2]:,}", item[3]])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Tabel Pendapatan Lama
    if pendapatan_history:
        elements.append(Paragraph("Pendapatan Lama (History):", styles['Heading2']))
        data = [['Keterangan', 'Total', 'Tanggal']]
        for item in pendapatan_history:
            data.append([item[1], f"Rp{item[2]:,}", item[3]])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Build PDF
    doc.build(elements)

    # Data untuk grafik
    labels = ['Pengeluaran Baru', 'Pengeluaran Lama', 'Pendapatan Baru', 'Pendapatan Lama']
    values = [
        sum([item[2] for item in pengeluaran]) if pengeluaran else 0,
        sum([item[2] for item in pengeluaran_history]) if pengeluaran_history else 0,
        sum([item[2] for item in pendapatan]) if pendapatan else 0,
        sum([item[2] for item in pendapatan_history]) if pendapatan_history else 0
    ]
    chart_buffer = plot_data(labels, values, title="Ringkasan Keuangan")

    return pdf_path, chart_buffer

def report(update: Update, context: CallbackContext):
    pdf_path, chart_buffer = generate_report()

    # Kirim file PDF
    with open(pdf_path, 'rb') as pdf_file:
        update.message.reply_document(document=pdf_file, filename=os.path.basename(pdf_path), caption="Berikut laporan keuangan Anda.")

    # Kirim chart sebagai gambar
    update.message.reply_photo(photo=chart_buffer, caption="Grafik ringkasan keuangan.")
