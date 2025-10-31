from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)
CORS(app)  # Frontend’in bu API’ye erişmesine izin verir (CORS politikası)

# 🌐 Veritabanı bağlantı adresi (ortam değişkeninden al, yoksa varsayılanı kullan)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://volkan:201eAcwsVd7cf1jyxQL2F1wn4VZ3FSbW@dpg-d3t90iur433s73b5q070-a.oregon-postgres.render.com/cloud_db_gwjr"
)

# 🔌 Veritabanına bağlanma fonksiyonu
def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("❌ Veritabanı bağlantı hatası:", e)
        return None

# 🧱 Tabloyu oluştur (ilk başta çağırmak için yardımcı fonksiyon)
def create_table_if_not_exists():
    conn = connect_db()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ziyaretciler (
                        id SERIAL PRIMARY KEY,
                        isim TEXT NOT NULL
                    )
                """)
        conn.close()

# 🧍 Ziyaretçi API Endpoint'i
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    if not conn:
        return jsonify({"error": "Veritabanı bağlantısı kurulamadı"}), 500

    try:
        with conn:
            with conn.cursor() as cur:
                # Tablo yoksa oluştur
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ziyaretciler (
                        id SERIAL PRIMARY KEY,
                        isim TEXT NOT NULL
                    )
                """)

                # POST isteği: Yeni ziyaretçi ekle
                if request.method == "POST":
                    data = request.get_json()
                    isim = data.get("isim") if data else None
                    if not isim:
                        return jsonify({"error": "İsim alanı boş olamaz"}), 400

                    cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
                    conn.commit()

                # GET isteği: Son 10 ziyaretçiyi getir
                cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
                isimler = [row[0] for row in cur.fetchall()]

        return jsonify(isimler)

    except Exception as e:
        print("⚠️ Sorgu hatası:", e)
        return jsonify({"error": "Bir hata oluştu"}), 500
    finally:
        conn.close()

# 🚀 Uygulamayı çalıştır
if __name__ == "__main__":
    create_table_if_not_exists()
    app.run(host="0.0.0.0", port=5001)
