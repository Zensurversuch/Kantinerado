# Kantinerado Backend
Für allgemeine Informationen über das Projekt bitte Readme des Projekts lesen

## Installation
Umd das Framework verwenden zu können muss anfangs eine virtuelle Umgebung erstellt und aktiviert werden.
Voraussetzung dafür ist Python installiert zu haben.

1. **Erstellen einer virtuellen Umgebung**
   - in den Ordner Backend wechseln
   - virtuelle Umgebung erstellen
        - Unter Unix/macOS:
            python3 -m venv .venv
        - Unter Windows:
            python -m venv .venv

2. **Interpreter der virtuellen Umgeung auswählen**
   - Die Taste "F1" drücken und "Python: Select Interpreter" auswählen
   - Interpreter mit Endung venv verwenden 
     wird der Interpreter der Umgebung nicht angezeigt Pfad des Interpreters angeben (Windows: ".venv\Scripts\python.exe")

3. **virtuelle Umgebung aktivieren**
    - Unter Unix/macOS:
        source venv/bin/activate
    - Unter Windows:
        venv\Scripts\activate

4. **Abhängigkeiten installieren**
    - pip install -r "requirements.txt"

## Ausführen der Anwendung
Um die Anwendung auszuführen muss folgender Befehl ausgeführt werden

    "flask run"
