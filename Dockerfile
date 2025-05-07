# 1. Leichtgewichtiges Python-Image
FROM python:3.13-slim

# 2. Arbeitsverzeichnis
WORKDIR /app

# 3. Nur Dependencies installieren (Cache sauber halten)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Restlichen Code kopieren
COPY . .

# 5. Production-WSGI: benutze Gunicorn statt Flask-Dev-Server
#    – WSGI-Callable ist in app.py: app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
