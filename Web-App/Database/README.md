# Datenbank

## Zu Testzwecken Datenbank Backup laden
Das DB Backup liegt [hier](Dummy_database.sql) und kann ![alt text](image-2.png) so geladen werden.
Das Andere DB-Backup [hier](Dummy_Database_Presentation.sql) ist zu Präsentationszwecken bereits mit Daten gefüllt. 


## Initialisieren der Tabellen
Wenn die Datenbank erstellt wurde müssen die Tabellen initialisiert werden. Wenn die Datenbank auf dem selben Rechner (local) läuft nimmnt man dieses [hier](initialize_db_local.py).
Wenn man eine Datenbank auf einem Server Remote ändern möchte nimmt man dieses [hier](initialize_db_server.py). Hier muss jedoch noch die IP des Serves eingefügt werden.
!Wichtig die Ausführung der Scripte zur Initialisierung müssen in diesem Ordner ausgeführt werden!

Die nötigen Bibliotheken werden bereits bei der Initialisierung des Backends [hier](/Web-App/Backend/README.md) installiert.

## Tabellen mit DBeaver einsehen befüllen
### Ausführen der SQL Skripte
Mit dem Datenbank Tool [DBeaver](https://dbeaver.io/) kann man SQL Skripte einfach in der Datenbank ausführen.
1. DBeaver herunterladen
2. Verbindung zur Datenbank herstellen
![DBeaver Bild Verbindung herstellen](image.png)
2.1 Auf das Connector Symbol klicken und PostgreSQL auswählsen  
2.2 Verbindungsdaten eingeben  
2.3 Verbindung testen drücken um zu schauen ob die Verbindung hergestellt werden kann  
2.4 Fertigstellen
