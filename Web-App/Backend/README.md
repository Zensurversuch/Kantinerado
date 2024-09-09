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

2. **Interpreter der virtuellen Umgebung auswählen**
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

## Swagger
    Diese Dokumentation beschreibt die Verwendung von Swagger zur Dokumentation von APIs in diesem Projekt. Swagger ist über die Route /swagger erreichbar und die Spezifikationen sind in der Datei swagger/swagger.json definiert.

### Verwendung
    Um auf die Swagger-Dokumentation zuzugreifen, navigieren Sie einfach zu http://<Ihre_Domain>/swagger in Ihrem Webbrowser.

### Spezifikationen
    Die Spezifikationen für die APIs sind in der Datei swagger/swagger.json definiert. Diese Datei enthält detaillierte Informationen über die verfügbaren Endpunkte, Parameter, Anfragemethoden und Antworten.

### Interaktion
    Durch die Verwendung von Swagger können Entwickler die verfügbaren APIs erkunden, deren Parameter verstehen und Beispiele für Anfragen und Antworten anzeigen. Dies erleichtert die Interaktion mit den APIs und ermöglicht eine schnellere Entwicklung von Anwendungen, die auf diesen APIs basieren.

### Weitere Informationen
    Für weitere Informationen zur Verwendung von Swagger und zur Interpretation der in swagger/swagger.json definierten Spezifikationen, besuchen Sie die offizielle Swagger-Dokumentation.

## Testen des Backends

1. **pytest installieren (optional)**
    Um pytest zu verwenden, muss dieses zuerst installiert werden.
    Dazu führen Sie den folgenden Befehl vorzugsweise in einer virtuellen Umgebung aus:
    ```bash
    pip install pytest
    ```

2. **pytest-con installieren (optional)**
    Wenn die Code-Coverage gemessen werden soll, muss das Plugin pytest-cov installiert sein.
    Dafür führen Sid den folgenden Befehl vorzugsweise in einer virtuellen Umgebung aus:
    ```bash
    pip install pytest-cov
    ```

2. **Docker Compose starten:**
    Führen Sie den folgenden Befehl in dem Ordner ("~/Web-App") aus:
    ```bash
    docker-compose -f docker-compose.test.yml up --build
    ```
    Dieser Befehl baut die Docker-Images und startet die Container gemäß der Konfiguration in der `docker-compose.yml`-Datei. Die Option `--build` wird verwendet, um sicherzustellen, dass das Backend und Frontend Image vor dem Start der Container neu erstellt wird, wodurch Änderungen am Code automatisch mit deployed werden.

3. **Tests starten**
    Um die Tests zu starten führen sie folgenden Befehl in dem Ordner ("~/Web-App") aus:
    ```bash
    pytest
    ```

4. **Code Coverage messen**
    Um die Code Coverage zu erfassen, muss anstelle des vorherigen Befehls der Folgender, in diesem Ordner ("~/Web-App"), ausgeführt werden:
    ```bash
    pytest --cov=Backend --cov-config=.coveragerc --cov-report=term
    ```
    Dieser Befehl führt die Tests aus und zeigt gleichzeitig die Code Coverage im Terminal an. Er misst, welcher Teil des Codes von den Tests abgedeckt ist.

    Um einen detaillierten Coverage-Bericht in HTML-Format zu erstellen kann folgender Befehl ausgeführt werden:
    ```bash
    pytest --cov=Backend --cov-config=.coveragerc --cov-report=html
    ```
    Danach kann der Bericht in einem Browser unter htmlcov/index.html betrachtet werden.


**Hinweise**
- Die PostgreSQL-Datenbank wird auf Port 5433 bereitgestellt.
- Sind die Container gestartet, können die Tests beliebig oft ausgeführt werden.