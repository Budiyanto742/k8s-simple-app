from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Konfigurasi Database
DB_HOST = "postgres-db"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "rahasiaku123"

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Buat tabel jika belum ada
        cur.execute('CREATE TABLE IF NOT EXISTS counter (id serial PRIMARY KEY, hits integer);')
        
        # 2. Ambil data hits, jika tidak ada masukkan data awal (id=1, hits=1)
        cur.execute('SELECT hits FROM counter WHERE id = 1;')
        row = cur.fetchone()
        
        if row is None:
            cur.execute('INSERT INTO counter (id, hits) VALUES (1, 1);')
            hits = 1
        else:
            hits = row[0] + 1
            cur.execute('UPDATE counter SET hits = %s WHERE id = 1;', (hits,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return f"""
        <div style='text-align: center; font-family: sans-serif; margin-top: 50px;'>
            <h1 style='color: #2e7d32;'>🚀 Lab CI/CD Berhasil!</h1>
            <p style='font-size: 1.2em;'>Status Database: <b>Terhubung</b></p>
            <div style='background: #f1f1f1; padding: 20px; display: inline-block; border-radius: 10px; border: 2px solid #2e7d32;'>
                <h2 style='margin: 0;'>Total Pengunjung</h2>
                <span style='font-size: 3em; font-weight: bold; color: #1565c0;'>{hits}</span>
            </div>
            <p style='color: #666;'>Data ini tersimpan permanen di PostgreSQL</p>
        </div>
        """
    except Exception as e:
        return f"<h1>Error Database!</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
