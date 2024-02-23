from flask import Flask, jsonify, request
from sqlalchemy import create_engine, MetaData
from DB_Repositories.UserRepository import UserRepository
import os

postgres_pw = os.getenv('POSTGRES_PW')

POSTGRES_URL = f"postgresql://postgres:{postgres_pw}@database/postgres"

app = Flask(__name__)
engine = create_engine(POSTGRES_URL)
metadata = MetaData()

user_repository = UserRepository(engine)

@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        lastName = data.get('lastName')
        firstName = data.get('firstName')
        role = data.get('role')
        allergies = data.get('allergies')

        if not (email and password and lastName and firstName and role):
            return jsonify({"message": "Missing required fields"}), 400

        if user_repository.create_user(email, password, lastName, firstName, role, allergies):
            return jsonify({"message": "User created successful"}), 201
        else:
            return jsonify({"message": "Failed to create user"}), 500


@app.route('/all_users')
def all_users():
    data = user_repository.get_all_users()
    if data:
        user_list = [{ 'userID': user.userID, 'email': user.email, 'lastName': user.lastName, 'firstName': user.firstName, 'role': user.role, 'allergies': user.allergies } for user in data]
        return jsonify(user_list)
    return jsonify({"message": "No users found"}), 404

@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = user_repository.get_user_by_id(user_id)
    if user:
        return user
    return jsonify({"message": "User not found"}), 404

@app.route('/user_password/<int:user_id>')
def get_user_password(user_id):
    user_pw = user_repository.get_password_for_user(user_id)
    if user_pw:
        return jsonify({"password": user_pw})
    return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')
