# 🐟 Fishora Bot - Telegram Bot Pencatatan Panen & Keuangan Ikan Maskoki

Fishora adalah Telegram bot yang digunakan oleh petani ikan maskoki untuk mencatat pengeluaran, pendapatan hasil panen, dan menghasilkan laporan PDF yang bisa diunduh langsung.

## 🚀 Fitur Utama

- ✍️ Input **pengeluaran** dan **pendapatan panen**
- 📦 Histori data tersimpan otomatis
- 📄 Generate laporan keuangan lengkap dalam format **PDF**
- 📊 Menampilkan grafik pengeluaran vs pendapatan
- 💾 Semua data disimpan dalam **SQLite database**
- 📂 Laporan disimpan otomatis ke folder `/reports`

---

## 🛠️ **Setup & Jalankan Bot**

### 1. Clone repository

Clone proyek ini ke mesin lokal Anda.

```bash
git clone https://github.com/username/fishora-bot.git
cd fishora-bot
pip install -r requirements.txt
```

### 2. Buat File .env
#### Gunakan installing depedencies dengan menggunakan command line 
```bash
pip install dotenv
```
#### Ganti Token Bot Manjadi 
##### BOT_TOKEN = "YOUR_BOT_TOKEN"

### 3. Running Bot Telegram 
```bash
python run.py
```

### Contoh Perintah Bot Telegram
```bash
/start - Memulai bot
/pengeluaran - Tambahkan data pengeluaran
/pendapatan - Tambahkan data pendapatan hasil panen
/report - Download laporan keuangan dalam format PDF
```

### Teknologi Yang Digunakan 
- Python 3.10+
- python-telegram-bot
- ReportLab (untuk PDF)
- Matplotlib (untuk visualisasi grafik)
- SQLite3 (untuk penyimpanan data)

### 🙌 Kontribusi
#### Jika kamu ingin berkontribusi, buatlah Pull Request! Jangan ragu untuk membuka Issue jika ada bug atau jika kamu ingin request fitur baru.

### 📄 Lisensi
MIT License © 2025 Dian Wicaksono
