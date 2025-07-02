import sqlite3
import os

os.makedirs("/data", exist_ok=True)

DB_NAME = "/data/fishora.db"

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

def get_all_pendapatan_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pendapatan_history ORDER BY tanggal DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------- Deleting  ----------------
def delete_all():
    items = ['pendapatan', 'pengeluaran', 'pendapatan_history', 'pengeluaran_history']
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for item in items:
            cursor.execute(f'DELETE FROM {item}')
            # Reset auto-increment ID untuk SQLite
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{item}'")
        conn.commit()
        print("Semua data dan ID berhasil direset!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()

def delete_item(table_name: str, item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Hapus data dari tabel utama
        cursor.execute(f'''
            DELETE FROM {table_name}
            WHERE id = ?
        ''', (item_id,))
        
        # Jika ingin pindahkan ke history (opsional)
        cursor.execute(f'''
            INSERT INTO {table_name}_history
            SELECT * FROM {table_name} WHERE id = ?
        ''', (item_id,))
        
        conn.commit()
        print(f"✅ Data ID {item_id} di {table_name} berhasil dihapus!")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal menghapus data: {str(e)}")
        return False
    finally:
        conn.close()

# ---------------- Utility ----------------

def move_to_history():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Mulai transaksi
        cursor.execute("BEGIN TRANSACTION")

        # 1. Pindahkan data pengeluaran ke history
        cursor.execute('''
            INSERT INTO pengeluaran_history (keterangan, harga, tanggal)
            SELECT keterangan, harga, tanggal FROM pengeluaran
        ''')
        cursor.execute("DELETE FROM pengeluaran")  # Kosongkan tabel utama

        # 2. Pindahkan data pendapatan ke history
        cursor.execute('''
            INSERT INTO pendapatan_history (keterangan, total, tanggal)
            SELECT keterangan, total, tanggal FROM pendapatan
        ''')
        cursor.execute("DELETE FROM pendapatan")  # Kosongkan tabel utama

        # 3. Reset auto-increment ID untuk tabel utama
        cursor.execute('''
            DELETE FROM sqlite_sequence 
            WHERE name IN ('pengeluaran', 'pendapatan')
        ''')

        # Commit semua perubahan
        conn.commit()
        print("✅ Data berhasil dipindahkan ke history + ID direset!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error saat memindahkan data: {str(e)}")
        raise  # Re-raise exception untuk handling di level atas

    finally:
        conn.close()
