# Kantinerado Backend
Für allgemeine Informationen über das Projekt bitte Readme des Projekts lesen

## Installation
Umd das Framework verwenden zu können muss anfangs eine virtuelle Umgebung erstellt und aktiviert werden.
Voraussetzung dafür ist Python installiert zu haben.

1. **Erstellen einer virtuellen Umgebung**
   - in den Ordner Backend wechseln
   - virtuelle Umgebung erstellen
        - Unter Unix/macOS:
            ```bash
            python3 -m venv .venv
            ```
        - Unter Windows:
            ```bash
            python -m venv .venv
            ```

2. **Interpreter der virtuellen Umgebung auswählen**
   - Die Taste "F1" drücken und "Python: Select Interpreter" auswählen
   - Interpreter mit Endung venv verwenden 
     wird der Interpreter der Umgebung nicht angezeigt Pfad des Interpreters angeben (Windows: ".venv\Scripts\python.exe")

3. **virtuelle Umgebung aktivieren**
    - Unter Unix/macOS:
        ```bash
        source venv/bin/activate
        ```
    - Unter Windows:
        ```bash
        venv\Scripts\activate
        ```

4. **Abhängigkeiten installieren**
   - ```bash
     pip install -r "requirements.txt"
     ```

## Ausführen der Anwendung
Um die Anwendung auszuführen muss folgender Befehl ausgeführt werden
```bash
flask run
```
## Swagger
Diese Dokumentation beschreibt die Verwendung von Swagger zur Dokumentation von APIs in diesem Projekt. Swagger ist über die Route /swagger erreichbar und die Spezifikationen sind in der Datei swagger/swagger.json definiert.

### Verwendung
    Um auf die Swagger-Dokumentation zuzugreifen, muss das Backend in der Development Konfiguration gestartet sein. Dafür geben Sie in Ihrer .env Datei unter environment "development" an. Danach können Sie einfach zu http://<Ihre_Backend_Domain>/swagger (Default Konfiguration: http://localhost:5000/swagger) in Ihrem Webbrowser navigieren, um auf die SwaggerUI, welche die Backend API-Routen dokumentiert, zuzugreifen.

    Da wir JWT verwenden, sind unsere Routen gesichert. Um Zugriff auf die gesperrten Routen zu erhalten, muss man oben rechts bei dem Schlosssymbol einen JWT-Token eingeben. Diesen Token erhält man über die Login-Route in Swagger, indem man die Zugangsdaten eines gültigen Nutzers eingibt und den JWT-Token aus der Antwort kopiert. Anschließend kann man sich oben rechts in der Swagger-UI mit diesem Token authentifizieren. Sollte allerdings kein Admin-User für den Login verwendet worden sein, kann es sein, dass manche Routen weiterhin gesperrt bleiben.

### Spezifikationen
Die Spezifikationen für die APIs sind in der Datei swagger/swagger.json definiert. Diese Datei enthält detaillierte Informationen über die verfügbaren Endpunkte, Parameter, Anfragemethoden und Antworten.

### Interaktion
Durch die Verwendung von Swagger können Entwickler die verfügbaren APIs erkunden, deren Parameter verstehen und Beispiele für Anfragen und Antworten anzeigen. Dies erleichtert die Interaktion mit den APIs und ermöglicht eine schnellere Entwicklung von Anwendungen, die auf diesen APIs basieren.

### Weitere Informationen
Für weitere Informationen zur Verwendung von Swagger und zur Interpretation der in swagger/swagger.json definierten Spezifikationen, besuchen Sie die offizielle Swagger-Dokumentation.

## Voraussetzungen für die Tests 

**Abhängigkeiten installieren:**

Um das Backend zu testen, müssen alle Abhängigkeiten installiert sein.
Führen Sie den folgenden Befehl aus, vorzugsweise in einer virtuellen Umgebung:
```bash
pip install -r "requirements.txt"
```

**Hinweis**: Die für die Tests benötigten Abhängigkeiten, wie `pytest` und `playwright`, sind nicht in der regulären `requirements.txt` aufgeführt, da diese Abhängigkeiten nur in der **Entwicklungs- und Testumgebung** benötigt werden.


**pytest installieren**
Um pytest zu verwenden, muss dieses zuerst installiert werden:
```bash
pip install pytest
```

**pytest-playwright installieren**
Um E2E-Tests mit pytest-playwright durchzuführen, muss das Plugin pytest-playwright installiert werden:
```bash
pip install pytest-playwright
```

**Playwright-Browser installieren**
Playwright benötigt bestimmte Browser (Chromium, Firefox, WebKit). Installieren Sie diese mit:
```bash
playwright install
```

**pytest-cov installieren (optional)**
Wenn die Code-Coverage gemessen werden soll, muss das Plugin pytest-cov installiert sein:
```bash
pip install pytest-cov
```