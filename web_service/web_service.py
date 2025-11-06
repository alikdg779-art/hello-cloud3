from flask import Flask, render_template_string, request, redirect
import requests, os

app = Flask(__name__)

# Mikro hizmet API adresini ortam değişkeninden al, yoksa varsayılan değeri kullan
API_URL = os.getenv("API_URL", "https://hello-cloud4.onrender.com")

HTML = """
<!doctype html>
<html>
<head>
    <title>Mikro Hizmetli Selam!</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        input { padding: 10px; font-size: 16px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; list-style-type: none; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>Adını yaz:</p>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
        <button type="submit">Gönder</button>
    </form>
    <h3>Ziyaretçiler:</h3>
    <ul>
        {% for ad in isimler %}
        <li>{{ ad }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        try:
            requests.post(f"{API_URL}/ziyaretciler", json={"isim": isim}, timeout=5)
        except requests.exceptions.RequestException as e:
            print("API isteğinde hata:", e)
        return redirect("/")

    try:
        resp = requests.get(f"{API_URL}/ziyaretciler", timeout=5)
        isimler = resp.json() if resp.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print("API'den veri alınamadı:", e)
        isimler = []

    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
