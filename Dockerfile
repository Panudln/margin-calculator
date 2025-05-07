# Verwende Python 3.13 slim als Basis
FROM python:3.13-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Nur requirements installieren (Cache sauber halten)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Restlichen Code kopieren
COPY . .

# Umgebungsvariablen für Flask
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Port, auf dem Flask lauscht
EXPOSE 5000

# Standard-Startbefehl
CMD ["flask", "run", "--host=0.0.0.0"]
