from flask import Flask, jsonify, request
from flasgger import Swagger
from role_permissions import get_permissions_for_role
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from sqlalchemy import create_engine, MetaData
from DB_Repositories import userRepository, dishesRepository, orderRepository, mealPlanRepository
import os
import base64

app = Flask(__name__)


# -------------------- Environment Variables -------------------------------
postgres_pw = os.getenv("POSTGRES_PW")
POSTGRES_URL = f"postgresql://postgres:{postgres_pw}@database/postgres"
testing = True
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  
# --------------------------------------------------------------------------

engine = create_engine(POSTGRES_URL)
metadata = MetaData()

jwt = JWTManager(app)
Swagger(app)

user_repo = userRepository.UserRepository(engine)
dish_repo = dishesRepository.DishRepository(engine)
meal_plan_repo = mealPlanRepository.MealPlanRepository(engine)
order_repo = orderRepository.OrderRepository(engine)



@app.route("/hello")
#@swag_from('swagger/hello.yml')  # Spezifiziere die Swagger-YAML-Datei für diesen Endpunkt
def hello():
    """
    Hello-Endpunkt
    ---
    responses:
      200:
        description: Nachricht, wenn die Berechtigung gewährt ist
      403:
        description: Nachricht, wenn die Berechtigung erforderlich ist
    """
    if not testing:
        current_user = get_jwt_identity()  # get_jwt_identity() returns userId
        current_role = "admin" # Implementieren von Datenbank
    else:
        current_user = "user1"
        current_role = "admin"
   
    current_permissions = set(get_permissions_for_role(current_role))
    if 'hello' in current_permissions:
        return jsonify(logged_in_as=current_user, message='Zugriff auf Geld gewährt! Hallo, Welt!')
    else:
        return jsonify(message='Zugriff mit Berechtigung für Geld erforderlich!'), 403

# USER ROUTES
@app.route('/login', methods=['POST'])
def login():
    """
    Benutzeranmelde-Endpunkt
    ---
    parameters:
      - name: username
        in: body
        type: string
        required: true
      - name: password
        in: body
        type: string
        required: true
    responses:
      200:
        description: Ein JWT-Token zur Authentifizierung
      400:
        description: Fehlende JSON-Anfrage oder fehlender Benutzername oder Passwort
      401:
        description: Falscher Benutzername oder Passwort
    """
    if not request.is_json:
        return jsonify({"msg": "Fehlendes JSON in der Anfrage"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Fehlender Benutzername oder Passwort"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Falscher Benutzername oder Passwort"}), 401
    
    #Meine Methoden
    # user_pw = user_repo.get_password_for_user(user_id)
    # if user_pw:
    #     return jsonify({"password": user_pw})
    # return jsonify({"message": "User not found"}), 404
    
    # !!!Methode entwickeln Alle daten von user for email!!!


    access_token = create_access_token(identity=userId)
    return jsonify(access_token=access_token), 200

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
    app.run(host='0.0.0.0', port=5000)
