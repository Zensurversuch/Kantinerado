# Datenbank

## Zu Testzwecken Datenbank Backup laden
Das DB Backup liegt [hier](DummyDatabase.sql) und kann ![alt text](image-2.png) so geladen werden.


## In der Produktion: Tabellen initialisieren
Wenn die Datenbank erstellt wurde müssen die Tabellen initialisiert werden. Dies wird mit dem Skript [initialize_db.py](initialize_db.py) gemacht. Wichtig ist das man dieses in diesem Ordner ausführt sodass das Passwort der Datenbank richtig gezogen wird.  
Wenn man dieses Skript ausführt wenn die Tabellen schon initialisiert sind führt dies zu keinem Fehler und auch die Daten die in der DB waren bleiben bestehen. Des Weiteren müssen die Python-Module "python-dotenv", "sqlalchemy" und "sqlalchemy" auf dem System installiert sein.

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
