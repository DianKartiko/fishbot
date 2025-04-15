import sqlite3
import os

DB_NAME = "fishora.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabel pengeluaran
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT NOT NULL,
            harga INTEGER NOT NULL,
            tanggal TEXT NOT NULL
        )
    ''')

    # Tabel pendapatan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pendapatan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT NOT NULL,
            total INTEGER NOT NULL,
            tanggal TEXT NOT NULL
        )
    ''')

    # History tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pengeluaran_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT,
            harga INTEGER,
            tanggal TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pendapatan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT,
            total INTEGER,
            tanggal TEXT
        )
    ''')

    conn.commit()
    conn.close()

# ---------------- Pengeluaran ----------------

def save_pengeluaran(keterangan, harga, tanggal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pengeluaran (keterangan, harga, tanggal)
        VALUES (?, ?, ?)
    ''', (keterangan, harga, tanggal))
    conn.commit()
    conn.close()

def get_all_pengeluaran():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pengeluaran ORDER BY tanggal DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def update_pengeluaran(id, keterangan, harga, tanggal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pengeluaran
        SET keterangan = ?, harga = ?, tanggal = ?
        WHERE id = ?
    ''', (keterangan, harga, tanggal, id))
    conn.commit()
    conn.close()

def delete_all_pengeluaran():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pengeluaran")
    conn.commit()
    conn.close()

def get_all_pengeluaran_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pengeluaran_history ORDER BY tanggal DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------- Pendapatan ----------------

def save_pendapatan(keterangan, total, tanggal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pendapatan (keterangan, total, tanggal)
        VALUES (?, ?, ?)
    ''', (keterangan, total, tanggal))
    conn.commit()
    conn.close()

def get_all_pendapatan():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pendapatan ORDER BY tanggal DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def update_pendapatan(id, keterangan, total, tanggal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pendapatan
        SET keterangan = ?, total = ?, tanggal = ?
        WHERE id = ?
    ''', (keterangan, total, tanggal, id))
    conn.commit()
    conn.close()

def delete_all_pendapatan():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pendapatan")
    conn.commit()
    conn.close()

def get_all_pendapatan_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pendapatan_history ORDER BY tanggal DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------- Utility ----------------

def move_to_history():
    conn = get_connection()
    cursor = conn.cursor()

    # Pindahkan pengeluaran ke history
    cursor.execute('''
        INSERT INTO pengeluaran_history (keterangan, harga, tanggal)
        SELECT keterangan, harga, tanggal FROM pengeluaran
    ''')
    cursor.execute("DELETE FROM pengeluaran")

    # Pindahkan pendapatan ke history
    cursor.execute('''
        INSERT INTO pendapatan_history (keterangan, total, tanggal)
        SELECT keterangan, total, tanggal FROM pendapatan
    ''')
    cursor.execute("DELETE FROM pendapatan")

    conn.commit()
    conn.close()
