from flask import Flask, jsonify, request
from sqlalchemy import create_engine, MetaData
from DB_Repositories import userRepository, dishesRepository, orderRepository, mealPlanRepository
import os
import base64


postgres_pw = os.getenv('POSTGRES_PW')

POSTGRES_URL = f"postgresql://postgres:{postgres_pw}@database/postgres"

app = Flask(__name__)
engine = create_engine(POSTGRES_URL)
metadata = MetaData()

user_repo = userRepository.UserRepository(engine)
dish_repo = dishesRepository.DishRepository(engine)
meal_plan_repo = mealPlanRepository.MealPlanRepository(engine)
order_repo = orderRepository.OrderRepository(engine)

@app.route("/hello")
def hello():
    return "Hello, World!"

# USER ROUTES
@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        lastName = data.get('lastName')
        firstName = data.get('firstName')
        role = data.get('role')

        if not (email and password and lastName and firstName and role):
            return jsonify({"message": "Missing required fields"}), 400

        if user_repo.create_user(email, password, lastName, firstName, role):
            return jsonify({"message": "User created successful"}), 201
        else:
            return jsonify({"message": "Failed to create user"}), 500

@app.route('/all_users')
def all_users():
    data = user_repo.get_all_users()
    if data:
        return jsonify(data)
    return jsonify({"message": "No users found"}), 404


@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = user_repo.get_user_by_id(user_id)
    if user:
        return user
    return jsonify({"message": "User not found"}), 404

@app.route('/user_allergy/<int:user_id>')
def get_allergies_for_user(user_id):
    allergy = user_repo.get_allergies_for_user(user_id)
    if allergy:
        return allergy
    return jsonify({"message": "User not found"}), 404

@app.route('/user_password/<int:user_id>')
def get_user_password(user_id):
    user_pw = user_repo.get_password_for_user(user_id)
    if user_pw:
        return jsonify({"password": user_pw})
    return jsonify({"message": "User not found"}), 404


# DISH ROUTES
@app.route('/dish/<int:dish_id>')
def get_dish_by_id(dish_id):
    dish = dish_repo.get_dish_by_id(dish_id)
    if dish:
        return dish
    return jsonify({"message": "Dish not found"}), 404

@app.route('/create_dish', methods=['POST'])
def create_dishes():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        ingredients = data.get('ingredients')
        dietary_category = data.get('dietary_category')
        meal_type = data.get('meal_type')
        image = data.get('image')
        allergies = data.get('allergies')

        if not (name and ingredients and dietary_category and meal_type):
            return jsonify({"message": "Missing required fields"}), 400

        image = base64.b64decode(image) if image else None

        if dish_repo.create_dish(name, ingredients, dietary_category, meal_type, image, allergies):
            return jsonify({"message": "Dish created successfully"}), 201
        else:
            return jsonify({"message": "Failed to create dish"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')
