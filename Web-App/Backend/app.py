from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, URL

POSTGRES_URL = URL.create(
    drivername="postgresql",
    username="postgres",
    password="test",
    host="database",
    port="5432",
    database="postgres"
)

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello, World! Du Hurensohn"

def get_users():
    engine = create_engine(POSTGRES_URL)

    metadata = MetaData()

    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String),
                  Column('email', String))

    metadata.create_all(engine)

    with engine.connect() as connection:
        result = connection.execute(users.select())
        users_data = []
        for row in result: 
            users_data.append({"id": row.id, "name": row.name, "email": row.email})

        return users_data

@app.route('/users')
def users():
    users_data = get_users()
    return f"Die Userdaten sind: {users_data}"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
