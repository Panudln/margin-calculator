# Dockerfile
FROM python:3.13-slim

# Arbeitsverzeichnis
WORKDIR /app

# Nur Abhängigkeiten kopieren & installieren (Cache sauber halten)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY . .

# Port freigeben
EXPOSE 5000

# Default-Befehl
CMD ["flask", "run", "--host=0.0.0.0"]
