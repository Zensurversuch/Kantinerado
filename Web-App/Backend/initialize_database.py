import hashlib
from sqlalchemy.orm import sessionmaker
from DB_Repositories.models import Base, User, Allergy
import time
import secrets
import os

# Postgres Database
def initialize_Postgres(engine):
    isDatabaseReady = False
    data_email = os.getenv('USER_EMAIL')
    data_password = os.getenv('USER_PASSWORD')
    data_last_name = os.getenv('USER_LAST_NAME')
    data_first_name = os.getenv('USER_FIRST_NAME')
    if (data_email and data_password and data_first_name and data_last_name):
        while not isDatabaseReady:
            try:
                Base.metadata.create_all(engine)

                Session = sessionmaker(bind=engine)
                session = Session()
                isDatabaseReady = True
            except Exception as e:
                print(f"PostgreSQL ist nicht erreichbar - versuche erneunt in einer Sekunde: {e}")
                time.sleep(1)
        try:
            #add admin user during initial setup
            if session.query(User).count() == 0:
            
                # Create the admin user
                    salt = secrets.token_hex()
                    user = User(
                    email = data_email,
                    password = hashlib.sha256((data_password + salt).encode('utf-8')).hexdigest(),
                    lastName = data_last_name,
                    firstName = data_first_name,
                    role = "admin",
                    salt = salt
                    )
                    session.add(user)
                    print("Admin Benutzer erfolgreich erstellt.")
            if session.query(Allergy).count() == 0:
                    allergies = [
                        Allergy (
                            name = "Gluten"
                        ),
                        Allergy (
                            name = "Laktose"
                        ),
                        Allergy (
                            name = "Ei"
                        ),
                        Allergy (
                            name = "Fisch"
                        ),
                        Allergy (
                            name = "Schalenfrüchte"
                        ),
                        Allergy (
                            name = "Nüsse"
                        ),
                        Allergy (
                            name = "Sulfite"
                        ),
                        Allergy (
                            name = "Krustentiere"
                        ),  
                    ]
                    session.add_all(allergies)
            session.commit()   
            print("Datenbank initialisiert.")
        except Exception as e:
            session.rollback()
            print(f"Admin Benutzer und Allergien konnten nicht angelegt werden: {e}")
        finally:    
            session.close()

    else:
        print("Umgebungsvariablen USER_EMAIL, USER_PASSWORD, USER_FIRST_NAME or USER_LAST_NAME wurden nicht angegeben. Datenbank Schema wird nicht automatisch aufgesetzt.")

#test Database
def initialize_test_database(engine):
    isDatabaseReady = False
    while not isDatabaseReady:
        try:
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            isDatabaseReady = True
        except Exception as e:
            print(f"PostgreSQL ist nicht erreichbar - versuche erneunt in einer Sekunde: {e}")
            time.sleep(1)
    try:
        #add admin user during initial setup
        if session.query(User).count() == 0:
            salt = secrets.token_hex()
            # Create the test users
            admin = User(
            userID = 1,
            email = 'admin@test.com',
            password = hashlib.sha256('admin_test'.encode('utf-8')).hexdigest(),
            salt = salt,
            lastName = 'admin',
            firstName = 'test',
            role = "admin"
            )
            worker = User(
            userID = 2,
            email = 'kantinenmitarbeiter@test.com',
            password = hashlib.sha256('kantinenmitarbeiter_test'.encode('utf-8')).hexdigest(),
            salt = salt,
            lastName = 'kantinenmitarbeiter',
            firstName = 'test',
            role = "kantinenmitarbeiter"
            )
            user = User(
            userID = 3,
            email = 'hungernder@test.com',
            password = hashlib.sha256('hungernder_test'.encode('utf-8')).hexdigest(),
            salt = salt,
            lastName = 'hungernder',
            firstName = 'test',
            role = "hungernde"
            )
            session.add(admin)
            session.add(worker)
            session.add(user)
            session.commit()
            print("Test Benutzer erfolgreich erstellt.")


        #Adding example allergies
        if session.query(Allergy).count() == 0:
            allergies = [
                Allergy(allergieID=1, name='TestAllergyOne'),
                Allergy(allergieID=2, name='TestAllergyTwo'),
            ]
            session.add_all(allergies)
            session.commit()
            print("Test-Allergien erfolgreich hinzugefügt.")
        print("Testdatenbank erfolgreich initialisiert")
    except Exception as e:
        print(f"Fehler beim Initialisieren der Testdatenbank: {e}")
    finally:
        session.close()