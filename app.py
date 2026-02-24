from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Konfigurasi Database - Ambil dari env atau sesuaikan dengan yang tadi berhasil
DB_HOST = "postgres-db"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "rahasiaku123" # Ganti dengan password yang tadi berhasil

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

# Inisialisasi Tabel
conn = get_db_connection()
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY, time timestamp DEFAULT CURRENT_TIMESTAMP);')
conn.commit()
cur.close()
conn.close()

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Tambah data kunjungan baru
        cur.execute('INSERT INTO visits (time) VALUES (DEFAULT);')
        conn.commit()
        
        # Hitung total kunjungan
        cur.execute('SELECT COUNT(*) FROM visits;')
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        return f"<h1>Lab CI/CD Berhasil!</h1><p>Anda adalah pengunjung ke-{count}. Data telah disimpan di Postgres!</p>"
    except Exception as e:
        return f"<h1>Error!</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
