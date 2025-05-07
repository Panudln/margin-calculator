# 🎉 Margin Calculator

![Logo](https://raw.githubusercontent.com/Panudln/margin-calculator/main/static/logo.png)

**Margin Calculator** ist eine schlanke Web-App, die dir dabei hilft, Einkaufspreise (Netto/Brutto) und Verkaufspreise mit Marge im Handumdrehen zu berechnen. Egal ob in Euro oder Prozent – gib einfach deine Werte ein und erhalte alle wichtigen Kennzahlen auf einen Blick.

---

## ✨ Features

* **EK Netto & EK Brutto**: Automatische Umrechnung zwischen Netto- und Brutto-Einkaufspreis anhand beliebiger MwSt.-Sätze.
* **Marge**: Aufschlag wählbar in % oder € – direkt auf den Netto-Preis.
* **Ergebnisübersicht**:

  * EK Netto
  * EK Brutto
  * VK Netto (inkl. Marge)
  * VK Brutto (inkl. Marge)
* **Modernes UI** mit Dark Mode (Standard)
* **Container-ready**: Starte per Docker-Compose oder lokal mit Flask.

---

## 🚀 Schnellstart

### Voraussetzungen

* Python 3.8+ (idealerweise 3.13)
* (Optional) Docker & Docker-Compose

### Lokal (ohne Docker)

1. Klone das Repo:

   ```bash
   git clone https://github.com/Panudln/margin-calculator.git
   cd margin-calculator
   ```
2. Virtuelle Umgebung anlegen & aktivieren:

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```
3. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```
4. App starten:

   ```bash
   flask run
   ```
5. Öffne im Browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Mit Docker

```bash
docker-compose up --build
```

Dann aufrufen: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🛠 Tech-Stack

* **Flask** – leichtgewichtiges Python-Web-Framework
* **HTML5 & CSS3** – modernes, responsives Frontend
* **Docker** – Containerisierung per Dockerfile
* **Docker-Compose** – Orchestrierung local/dev

---

## 🤝 Contributing

Beiträge willkommen! Öffne gerne Issues oder Pull Requests. 🙌

---

## 📄 License

MIT © 2025 [Panudln](https://github.com/Panudln)
