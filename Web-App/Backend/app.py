from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import create_engine, MetaData
from DB_Repositories import userRepository, dishesRepository, orderRepository, mealPlanRepository
import os
import base64
from flask_cors import CORS
from decorators import permission_check
import hashlib
app = Flask(__name__)

# -------------------------- Environment Variables ------------------------------------------------------------------------------------------------------------------------------------------
SWAGGER_URL = "/swagger"
API_URL = "/swagger/swagger.json"
POSTGRES_URL = f"postgresql://postgres:{os.getenv('POSTGRES_PW')}@database/postgres"
app.config["JWT_SECRET_KEY"] = f"{os.getenv('JWT_SECRET_KEY')}"

testing = False
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


engine = create_engine(POSTGRES_URL)
metadata = MetaData()

jwt = JWTManager(app)
CORS(app)

user_repo = userRepository.UserRepository(engine)
dish_repo = dishesRepository.DishRepository(engine)
meal_plan_repo = mealPlanRepository.MealPlanRepository(engine)
order_repo = orderRepository.OrderRepository(engine)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Kantinerado"
    },
)

app.register_blueprint(swaggerui_blueprint)

@app.route('/swagger/swagger.json')
def send_swagger_json():
    return send_from_directory('swagger', 'swagger.json')


# -------------------------- Client Routes ---------------------------------------------------------------------------------------------------------------------------------------
@app.route("/hello")
@jwt_required()
@permission_check(user_repo)
def hello():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user, message='Zugriff auf Hello gestattet! Hallo, Welt!')



# -------------------------- User Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Fehlendes JSON in der Anfrage"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if not email or not password:
        return jsonify({"msg": "Fehlender Benutzername oder Passwort"}), 400

    user_data = user_repo.get_user_by_email(email)

    if user_data and (hashed_pw == user_data["password"]):
        access_token = create_access_token(identity=user_data["userID"])
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Falscher Benutzername oder Passwort"}), 401

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    lastName = data.get('lastName')
    firstName = data.get('firstName')
    allergies = data.get('allergies')
    if not (email and password and lastName and firstName):
        return jsonify({"message": "Missing required fields"}), 400

    if user_repo.get_user_by_email(email):
        return jsonify({"message": f"User with the email {email} already exists"}), 500

    ret_value = user_repo.create_user(email, password, lastName, firstName, "hungernde", allergies)
    if not ret_value:   # If ret_value is empty no allergies were missing
        return jsonify({"message": "User created successful"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({"message": f"User created successful, but the allergies {ret_value} aren't present in the database"}), 201
    elif ret_value == False:
        return jsonify({"message": "Failed to create user"}), 500

@app.route('/create_user_as_admin', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_user_as_admin():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    lastName = data.get('lastName')
    firstName = data.get('firstName')
    role = data.get('role')
    allergies = data.get('allergies')
    if not (email and password and lastName and firstName and role):
        return jsonify({"message": "Missing required fields"}), 400

    if role not in ["hungernde", "admin", "kantinenmitarbeiter"]:
        return jsonify({"message": f"the role: {role} , doesn't exist"}), 400

    if user_repo.get_user_by_email(email):
        return jsonify({"message": f"User with the email {email} already exists"}), 500

    ret_value = user_repo.create_user(email, password, lastName, firstName, role, allergies)
    if not ret_value:   # If ret_value is empty no allergies were missing
        return jsonify({"message": "User created successful"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({"message": f"User created successful, but the allergies {ret_value} aren't present in the database"}), 201
    elif ret_value == False:
        return jsonify({"message": "Failed to create user"}), 500

@app.route('/all_users')
@jwt_required()
@permission_check(user_repo)
def all_users():
    data = user_repo.get_all_users()
    if data:
        return jsonify(data)
    return jsonify({"message": "No users found"}), 404

@app.route('/user_by_id/<int:user_id>')
@jwt_required()
@permission_check(user_repo)
def user_by_id(user_id):
    user = user_repo.get_user_by_id(user_id)
    if user:
        return user
    return jsonify({"message": "User not found"}), 404

@app.route('/user_by_email/<string:email>')
@jwt_required()
@permission_check(user_repo)
def user_by_email(email):
    user = user_repo.get_user_by_email(email)
    if user:
        return user
    return jsonify({"message": "User not found"}), 404

@app.route('/allergy_by_userid/<int:user_id>')
@jwt_required()
@permission_check(user_repo)
def allergy_by_userid(user_id):
    user_data = user_repo.get_user_by_id(user_id)
    if user_data:
        return user_data["allergies"]
    return jsonify({"message": "User not found"}), 404


# -------------------------- Dish Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/dish_by_id/<int:dish_id>')
@jwt_required()
@permission_check(user_repo)
def dish_by_id(dish_id):
    dish = dish_repo.get_dish_by_id(dish_id)
    if dish:
        return dish
    return jsonify({"message": "Dish not found"}), 404

@app.route('/create_dish', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_dish():
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

    ret_value = dish_repo.create_dish(name, ingredients, dietary_category, meal_type, image, allergies)
    if not ret_value:   # If ret_value is empty no allergies were missing
        return jsonify({"message": "Dish created successful"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({"message": f"Dish created successful, but the allergies {ret_value} aren't present in the database"}), 201
    elif ret_value == False:
        return jsonify({"message": "Failed to create Dish"}), 500


# -------------------------- Order Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/create_order', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_order():
    data = request.json
    userID = get_jwt_identity()
    mealPlanID = data.get('mealPlanID')
    amount = data.get('amount')

    if not (userID and mealPlanID and amount):
        return jsonify({"message": "Missing required fields"}), 400

    if order_repo.is_order_already_created(userID, mealPlanID):
        return jsonify({"message": "This order was already created"}), 500
    
    if order_repo.create_order(userID, mealPlanID, amount):
        return jsonify({"message": "Order created successful"}), 201
    return jsonify({"message": "Failed to create Order"}), 500

@app.route('/orders_by_user/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check(user_repo)
def orders_by_user(start_date, end_date):
    current_user = get_jwt_identity()
    orders = order_repo.get_orders_by_userid(current_user, start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({"message": "No orders for you found in the selected timespan"}), 404
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
