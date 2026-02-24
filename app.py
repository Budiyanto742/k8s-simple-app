from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def hello():
    db_host = os.getenv('DB_HOST', 'postgres-db')
    db_name = os.getenv('DB_NAME', 'postgres')
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASS', 'password_anda') # Sesuaikan dengan password DB kemarin

    try:
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
        status = "BERHASIL terhubung ke Postgres!"
        conn.close()
    except Exception as e:
        status = f"GAGAL konek ke DB: {e}"

    return f"<h1>Hello dari Kubernetes CI/CD!</h1><p>Status Database: {status}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Trigger CI/CD
# Update robot
