# Verwende das schlanke Python-Image
FROM python:3.13-slim

# Arbeitsverzeichnis
WORKDIR /app

# Nur dependencies installieren (Cache sauber halten)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Restlichen Quellcode kopieren
COPY . .

# Port freigeben
EXPOSE 5000

# Mit Gunicorn starten
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
