from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# PostgreSQL connection string
POSTGRES_URL = 'postgresql://postgres:test@localhost:5432/postgres'

def initialize_database():
    engine = create_engine(POSTGRES_URL)

    metadata = MetaData()

    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String),
                  Column('email', String))

    metadata.create_all(engine)

    # Optionally, insert some example data
    with engine.connect() as connection:
        connection.execute(users.insert().values(name='John Doe', email='john@example.com'))
        connection.execute(users.insert().values(name='Jane Smith', email='jane@example.com'))
        connection.commit()

    print("Daten wurden erfolgreich in die Datenbank eingefügt.")

if __name__ == "__main__":
    initialize_database()
