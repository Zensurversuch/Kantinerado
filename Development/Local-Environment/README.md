**README für Docker Compose Setup (Backend-Datenbank)**

Dieses Docker-Compose-Setup ermöglicht es, eine einfache Webanwendung mit einer Backend-API und einer PostgreSQL-Datenbank lokal zu betreiben. Hier ist eine kurze Anleitung, wie Sie das Setup starten können:

**Voraussetzungen:**
- Docker und Docker Compose müssen auf Ihrem System installiert sein.

**Schritte zum Starten der Anwendung:**

2. **Konfiguration anpassen (optional):**
    Sie können die Konfiguration der Datenbank in der `docker-compose.yml`-Datei ändern, einschließlich des Benutzernamens, Passworts und des Datenbanknamens. Standardmäßig sind die Werte auf `postgres`, `test` und `postgres` eingestellt.

3. **Docker Compose starten:**
    Führen Sie den folgenden Befehl in diesem Ordner aus:
    ```bash
    docker-compose up --build
    ```
    Dieser Befehl baut die Docker-Images und startet die Container gemäß der Konfiguration in der `docker-compose.yml`-Datei. Die Option `--build` wird verwendet, um sicherzustellen, dass die Images vor dem Start der Container neu erstellt werden.

5. **Aufräumen:**
    Um die Docker-Container zu stoppen und aufzuräumen, verwenden Sie den folgenden Befehl:
    ```bash
    docker-compose down
    ```
    Dieser Befehl stoppt und entfernt die gestarteten Container.

**Hinweise:**
- Der Backend-Service wird auf Port 5000 des Hosts bereitgestellt, während die PostgreSQL-Datenbank auf Port 5432 bereitgestellt wird. Diese Ports können in der `docker-compose.yml`-Datei geändert werden, wenn sie bereits von anderen Anwendungen verwendet werden.
- Wenn die Datenbank von außen nicht erreichbar sein soll, können Sie die entsprechenden Ports in der `docker-compose.yml`-Datei auskommentieren, wie in den Kommentaren beschrieben.
