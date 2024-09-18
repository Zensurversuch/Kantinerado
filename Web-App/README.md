# README für Docker Compose Setup

Dieses Docker-Compose-Setup ermöglicht es, eine einfache Webanwendung mit einer Backend-API und einer
PostgreSQL-Datenbank lokal zu betreiben. Hier ist eine kurze Anleitung, wie Sie das Setup starten können:

## Voraussetzungen:

- Stellen Sie sicher, dass Docker und Docker Compose auf Ihrem System installiert sind.
- !!!Erstellen Sie eine `.env`-Datei in diesem Ordner mit dem folgenden Inhalt:
   ```text
   # Diese Datei kann Variablen für Docker speichern  
    JWT_SECRET_KEY=<key>  # Setzen Sie hier das Secret für den JWT Token
    ENVIRONMENT=<development || production>         # Zum lokalen test development, auf dem server production
    #PostgreSQL variablen
    POSTGRES_PASSWORD=<Passwort>                            # Setzen Sie hier das Passwort 
    USER_EMAIL= <E-mail>                                    # Setze die E-mail für den erstern Kantinerado Admin Benutzer (optional)
    USER_PASSWORD = <Passwort>                              # Setze das Password für den erstern Kantinerado Admin Benutzer (optional)
    USER_LAST_NAME=<Nachnamen>                              # Setze das Nachnamen für den erstern Kantinerado Admin Benutzer (optional)
    USER_FIRST_NAME=<Vornamen>                              # Setze das Vornamen für den erstern Kantinerado Admin Benutzer (optional)
   
   ```

## Schritte zum Starten der Anwendung:

1. **Docker Compose starten:**
   Führen Sie den folgenden Befehl in diesem Ordner ("~/Web-App") aus:
    ```bash
    docker-compose up --build
    ```
   Dieser Befehl baut die Docker-Images und startet die Container gemäß der Konfiguration in der `docker-compose.yml`
   -Datei. Die Option `--build` wird verwendet, um sicherzustellen, dass das Backend und Frontend Image vor dem Start
   der Container neu erstellt wird, wodurch Änderungen am Code automatisch mit deployed werden.

2. **Aufräumen:**
   Um die Docker-Container zu stoppen und aufzuräumen, verwenden Sie den folgenden Befehl:
    ```bash
    docker-compose down
    ```
   Dieser Befehl stoppt und entfernt die gestarteten Container.

**Hinweise:**

- Der Backend-Service wird auf Port 5000 des Hosts bereitgestellt, während die PostgreSQL-Datenbank auf Port 5432
  bereitgestellt wird. Diese Ports können in der `docker-compose.yml`-Datei geändert werden, wenn sie bereits von
  anderen Anwendungen verwendet werden.
- Wenn die Datenbank von außen nicht erreichbar sein soll, können Sie die entsprechenden Ports in der
  `docker-compose.yml`-Datei auskommentieren, wie in den Kommentaren beschrieben.

## Nach dem Starten der Datenbank Initialisierung duchführen

Wie dies geht ist in der Database [README.md](./Database/README.md) beschrieben.

## Ausführen der Tests:

**Hinweis**:
Die Installation der Voraussetzungen für die Tests ist im Backend-Ordner beschrieben. Bitte stellen Sie sicher, dass Sie die entsprechenden Schritte in der [README.md](./Backend/README.md) des Backends befolgen, um die Tests erfolgreich auszuführen.

**Docker Compose starten**

```bash
docker-compose -f docker-compose.test.yml up --build
```

Dieser Befehl baut die Docker-Images und startet die Container gemäß der Konfiguration in der `docker-compose.yml`-Datei. Die Option `--build` stellt sicher, dass das Backend- und Frontend-Image vor dem Start der Container neu erstellt wird, wodurch Änderungen am Code automatisch übernommen werden.

**Tests starten**
Um die Tests zu starten, führen Sie folgenden Befehl aus:

```bash
pytest
```

**Spezielle pytest-Konfigurationen:**

- Für **E2E-Tests**:
    ```bash
    pytest -c pytest_e2e.ini
    ```
- Für **UI-Tests**
    ```bash
    pytest -c pytest_ui.ini
    ```
- Für **Unit-Tests**:
    ```bash
    pytest -c pytest_unit.ini
    ```

4. **Code Coverage messen**
Um die Code Coverage zu erfassen, führen Sie folgenden Befehl aus:
    ```bash
    pytest --cov=Backend --cov-config=.coveragerc --cov-report=term
    ```

   Um einen detaillierten Coverage-Bericht im HTML-Format zu erstellen, führen Sie diesen Befehl aus:
    ```bash
    pytest --cov=Backend --cov-config=.coveragerc --cov-report=html
    ```
   Danach kann der Bericht im Browser unter `htmlcov/index.html` betrachtet werden.

## Hinweise

- Die PostgreSQL-Datenbank wird in der Testumgebung auf Port 5433 bereitgestellt.
- Sobald die Container gestartet sind, können die Tests beliebig oft ausgeführt werden.