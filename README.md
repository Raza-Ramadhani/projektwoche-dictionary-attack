# R.A.Z.A. 2.0 - Kryptoanalyse & Wörterbuch-Angriff Suite
*Rapid Algorithmic Zone Analyzer* 
Projektwoche Kryptoanalyse Gym 3

---

## Übersicht

R.A.Z.A. 2.0 vereint drei zentrale Werkzeuge der klassischen und modernen Kryptoanalyse in einer einheitlichen Python-Anwendung im Cyberpunk/Terminal-Look:

1. **⚡ Wörterbuch-Angriff (Dictionary Attack)**:
   - Schnelles Durchsuchen von Wortlisten (`passwords.txt`)
   - Unterstützt **SHA-1**, **SHA-256** und **MD5**
   - Thread-sichere Ausführung mit Live-Telemetrie (Geschwindigkeit, Fortschritt, Dauer)
   - Sofortiges Abbrechen möglich

2. **🔑 Hash-Generator**:
   - Erzeugt parallel SHA-1, SHA-256 und MD5-Hashes aus beliebigem Klartext
   - 1-Klick-Übernahme direkt in das Wörterbuch-Angriffswerkzeug
   - Kopieren in die Zwischenablage

3. **🏛️ Caesar-Kryptoanalyse & Chiffre**:
   - **Automatischer Kryptoanalyse-Angriff**: Durchsucht alle 26 Schlüssel und bewertet Treffer anhand einer integrierten deutschen und englischen Häufigkeits-Wörterliste
   - **Manuelles Ver- & Entschlüsseln**: Interaktiver Schlüssel-Schieberegler (0–25)

---

## Schnellstart mit `uv`

### 1. Grafische Oberfläche (GUI) starten
```bash
# Über das installierte Script
uv run dictionary-attack

# Oder über das Alias
uv run raza

# Oder direkt über das Hauptskript
uv run main.py
```

### 2. Interaktives Terminal-Menü starten
Falls keine grafische Oberfläche gewünscht ist (z.B. im reinen Terminal):
```bash
uv run dictionary-attack --cli
```

### 3. Direkte CLI-Befehle

- **Caesar-Geheimtext automatisch knacken:**
  ```bash
  uv run dictionary-attack --caesar-crack "JXLQLSLJV UHVHQW ZDWHU, PDFDTXHV GLVOLNH VRBEHDQV"
  ```

- **Hashes aus einem Wort erzeugen:**
  ```bash
  uv run dictionary-attack --hash "geheim123"
  ```

- **Wörterbuch-Angriff direkt im Terminal:**
  ```bash
  uv run dictionary-attack --crack "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8" --algo sha1
  ```

- **Caesar ver- oder entschlüsseln:**
  ```bash
  uv run dictionary-attack --caesar-encrypt "HALLO WELT" --key 3
  uv run dictionary-attack --caesar-decrypt "KDOOR ZHOW" --key 3
  ```

---

## Projektstruktur

```
Project/
├── pyproject.toml              # UV / Python Projektkonfiguration
├── README.md                   # Projektdokumentation
├── main.py                     # Direkter Einstiegspunkt
└── src/
    └── dictionary_attack/
        ├── __init__.py         # Modulexporte
        ├── __main__.py         # python -m dictionary_attack Unterstützung
        ├── cli.py              # CLI Argument-Parser & Terminal-Menü
        ├── cracker.py          # Wiederverwendbare Dictionary-Attack-Engine
        ├── hashing.py          # SHA-1, SHA-256, MD5 Hilfsfunktionen
        ├── caesar.py           # Caesar-Verschlüsselung & automatischer Knacker
        ├── caesar_decrypt.py   # Einzeltestskript für Caesar-Kryptoanalyse
        ├── generate_hash.py    # Einzeltestskript für Hash-Generierung
        ├── passwords.txt       # Passwort-Wortliste (nicht im Repo, siehe .gitignore)
        └── gui/
            ├── __init__.py
            └── app.py          # Tkinter R.A.Z.A. 2.0 GUI-Suite
```
