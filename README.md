<!-- Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)  
# 🎉 Margin Calculator

**Margin Calculator** ist eine schlanke Web-App, die dir hilft, Einkaufspreise (Netto/Brutto) und Verkaufspreise mit Marge blitzschnell zu berechnen – wahlweise in Euro oder Prozent. 

---

## ✨ Features

- **EK Netto ↔ EK Brutto**  
  Automatische Umrechnung anhand beliebiger MwSt.-Sätze  
- **Marge**  
  Aufschlag wählbar in % oder € und sofort auf den Netto-Preis angewendet  
- **Ergebnisübersicht**  
  - EK Netto  
  - EK Brutto  
  - VK Netto (inkl. Marge)  
  - VK Brutto (inkl. Marge)  
- **Modernes UI**  
  Dark-Mode (Standard)  
- **Container-ready**  
  Lokal mit Flask oder per Docker-Compose starten  

---

## 🚀 Schnellstart

### Voraussetzungen

- Python 3.8+ (idealerweise 3.13)  
- (Optional) Docker & Docker-Compose  

### Lokal (ohne Docker)

```bash
git clone https://github.com/Panudln/margin-calculator.git
cd margin-calculator

# Virtuelle Umgebung anlegen & aktivieren
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
flask run
````

→ Öffne im Browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Mit Docker

```bash
docker-compose up --build
# oder
docker compose up --build
```

Führe den Befehl unbedingt im Projekt-Stammverzeichnis aus.
Andernfalls kann Compose die **Dockerfile** nicht finden und meldet Fehler wie
`failed to read dockerfile: ... Dockerfile: no such file or directory`.

Wenn du stattdessen `docker stack deploy` (z.B. über Portainer) nutzt, baue
das Image vorher lokal und gib es in der Compose-Datei unter `image:` an –
Swarm ignoriert nämlich `build:`-Anweisungen.

→ Öffne im Browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## ⚙️ Configuration

Umgebungsvariablen (nur bei Bedarf):

```env
FLASK_APP=app
FLASK_ENV=production
```

Oder in `docker-compose.yml`:

```yaml
services:
  app:
    environment:
      - FLASK_APP=app
      - FLASK_ENV=production
```

---

## 🛠 Tech-Stack

* **Flask** – leichtgewichtiges Python-Web-Framework
* **HTML5 & CSS3** – modernes, responsives Frontend
* **Docker** – Containerisierung
* **Docker-Compose** – Orchestrierung für Dev & Prod

---

## 📄 License

MIT © 2025 Panudln

---

## 🤝 Contributing

Beiträge willkommen! Öffne gerne Issues oder Pull Requests. 🙌
