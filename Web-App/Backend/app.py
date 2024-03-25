from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import create_engine, MetaData
from DB_Repositories import userRepository, dishesRepository, orderRepository, mealPlanRepository, allergyRepository
from api_messages import get_api_messages
import os
import base64
from flask_cors import CORS
from decorators import permission_check
import hashlib
from datetime import datetime, timedelta


app = Flask(__name__)

# -------------------------- Environment Variables ------------------------------------------------------------------------------------------------------------------------------------------
SWAGGER_URL = "/swagger"
API_URL = "/swagger/swagger.json"
POSTGRES_URL = f"postgresql://postgres:{os.getenv('POSTGRES_PW')}@database/postgres"
app.config["JWT_SECRET_KEY"] = f"{os.getenv('JWT_SECRET_KEY')}"

api_message_descriptor = "response"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


engine = create_engine(POSTGRES_URL)
metadata = MetaData()

jwt = JWTManager(app)
CORS(app)

user_repo = userRepository.UserRepository(engine)
dish_repo = dishesRepository.DishRepository(engine)
meal_plan_repo = mealPlanRepository.MealPlanRepository(engine)
order_repo = orderRepository.OrderRepository(engine)
allergy_repo = allergyRepository.AllergyRepository(engine)

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


# -------------------------- User Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fehlendes JSON in der Anfrage"}), 400

    data_email = request.json.get('email', None)
    data_password = request.json.get('password', None)
    hashed_pw = hashlib.sha256(data_password.encode('utf-8')).hexdigest()

    if not data_email or not data_password:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fehlender Benutzername oder Passwort"}), 400

    user_data = user_repo.get_user_by_email(data_email)

    if user_data and (hashed_pw == user_data["password"]):
        access_token = create_access_token(identity=user_data["userID"], expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token, userID = user_data["userID"], role = user_data["role"]), 200
    else:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Falscher Benutzername oder Passwort"}), 401

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    data_email = data.get('email')
    data_password = data.get('password')
    data_lastName = data.get('lastName')
    data_firstName = data.get('firstName')
    data_allergies = data.get('allergies')
    if not (data_email and data_password and data_lastName and data_firstName):
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    if user_repo.get_user_by_email(data_email):
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Benutzer mit der E-Mail {data_email} exisitiert bereits"}), 500

    ret_value = user_repo.create_user(data_email, data_password, data_lastName, data_firstName, "hungernde", data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({api_message_descriptor: f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({api_message_descriptor: f"{get_api_messages.WARNING.value}Benutzer erfolgreich erstellt, aber die folgenden Allergien {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Benutzer konnte nicht erstellt werden"}), 500

@app.route('/create_user_as_admin', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_user_as_admin():
    data = request.json
    data_email = data.get('email')
    data_password = data.get('password')
    data_lastName = data.get('lastName')
    data_firstName = data.get('firstName')
    data_role = data.get('role')
    data_allergies = data.get('allergies')
    if not (data_email and data_password and data_lastName and data_firstName and data_role):
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    if data_role not in ["hungernde", "admin", "kantinenmitarbeiter"]:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value} Die Rolle {data_role} , existiert nicht"}), 400

    if user_repo.get_user_by_email(data_email):
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Benutzer mit der E-Mail {data_email} exisitiert bereits"}), 500

    ret_value = user_repo.create_user(data_email, data_password, data_lastName, data_firstName, data_role, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({api_message_descriptor: f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({api_message_descriptor: f"{get_api_messages.WARNING.value}Benutzer erfolgreich erstellt, aber die folgenden Allergien {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Benutzer konnte nicht erstellt werden"}), 500

@app.route('/all_users')
@jwt_required()
@permission_check(user_repo)
def all_users():
    data = user_repo.get_all_users()
    if data:
        return jsonify(data)
    return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404

@app.route('/user_by_id/<int:user_id>')
@jwt_required()
@permission_check(user_repo)
def user_by_id(user_id):
    user = user_repo.get_user_by_id(user_id)
    if user:
        return user
    return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404

@app.route('/user_by_email/<string:email>')
@jwt_required()
@permission_check(user_repo)
def user_by_email(email):
    user = user_repo.get_user_by_email(email)
    if user:
        return user
    return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404

@app.route('/allergy_by_userid/<int:user_id>')
@jwt_required()
@permission_check(user_repo)
def allergy_by_userid(user_id):
    user_data = user_repo.get_user_by_id(user_id)
    if user_data:
        if user_data["allergies"] != None:
            return user_data["allergies"]  
        else:
            return jsonify({api_message_descriptor:  f"{get_api_messages.WARNING.value}Keine Allergien für diesen Benutzer hinterlegt"}), 404
    return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404


@app.route('/set_user_allergies',  methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def set_user_allergies():
    data = request.json
    jwt_userID = get_jwt_identity()
    data_allergies = data.get('allergies')
    ret_value = user_repo.set_user_allergies_by_id(jwt_userID, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({api_message_descriptor:  f"{get_api_messages.SUCCESS.value}Allergien erfolgreich angepasst"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing or the user wasn't found
        if ret_value == "User not found!":
            return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404
        return jsonify({api_message_descriptor: f"{get_api_messages.WARNING.value}Allergien erfolgreich angepasst, aber die folgenden Allergien {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Allergien konnten nicht angepasst werden"}), 500

# -------------------------- Allergy Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/allergy_by_id/<int:allergy_id>')
def allergy_by_id(allergy_id):
    allergy = allergy_repo.get_allergie_by_id(allergy_id)
    if allergy:
        return allergy
    return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Allergie nicht gefunden"}), 404

@app.route('/all_allergies')
def all_allergies():
    data = allergy_repo.get_all_allergies()
    if data:
        return jsonify(data)
    return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Keine Allergien gefunden"}), 404


# -------------------------- Dish Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/dish_by_id/<int:dish_id>')
@jwt_required()
@permission_check(user_repo)
def dish_by_id(dish_id):
    dish = dish_repo.get_dish_by_id(dish_id)
    if dish:
        return dish
    return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Gericht nicht gefunden"}), 404

@app.route('/dish_by_name/<string:dish_name>')
@jwt_required()
@permission_check(user_repo)
def dish_by_name(dish_name):
    dish = dish_repo.get_dish_by_name(dish_name)
    if dish:
        return dish
    return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Gericht nicht gefunden"}), 404

@app.route('/dish_by_mealType/<string:dish_mealType>')
def dish_by_mealType(dish_mealType):
    dishes = dish_repo.get_dishes_by_mealType(dish_mealType)
    if dishes:
        return dishes
    return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Keine Gerichte gefunden"}), 404


@app.route('/create_dish', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_dish():
    data = request.json
    data_name = data.get('name')
    data_price = data.get('price')
    data_ingredients = data.get('ingredients')
    data_dietaryCategory = data.get('dietaryCategory')
    data_mealType = data.get('mealType')
    data_image = data.get('image')
    data_allergies = data.get('allergies')

    if not (data_name and data_price and data_dietaryCategory and data_mealType):
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    if dish_repo.get_dish_by_name(data_name):
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Gericht existiert bereits"}), 400

    decoded_image = base64.b64decode(data_image) if data_image else None

    ret_value = dish_repo.create_dish(data_name, data_price, data_dietaryCategory, data_mealType, data_ingredients, decoded_image, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({api_message_descriptor:  f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({api_message_descriptor: f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allerigie {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Gericht konnte nicht erstellt werden"}), 500


# -------------------------- Order Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/create_order', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_order():
    data = request.json
    jwt_userID = get_jwt_identity()
    data_Orders = data.get('orders')
    mealPlan_ids = []

    if not data_Orders:
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Keine Bestellungen im JSON gefunden"}), 400

    for order in data_Orders:
        mealPlanID = order.get('mealPlanID')
        amount = order.get('amount')
        if (mealPlanID == None and amount == None):
            return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400
        mealPlan_ids.append(mealPlanID)

    timestamp = datetime.today()
    if (timestamp.weekday() == 3 and timestamp.hour >= 18) or (timestamp.weekday() > 3):
        mealPlanDates = meal_plan_repo.get_mealPlan_dates_by_ids(mealPlan_ids)
        if mealPlanDates:
            monday = timestamp - timedelta(days=timestamp.weekday()) + timedelta(days=7)
            sunday = monday + timedelta(days=6)
            if any(datetime.strptime(mealPlanDate, "%Y-%m-%d") < sunday for mealPlanDate in mealPlanDates): 
                return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Es können keine Bestellungen mehr nach Donnerstag 16 Uhr aufgegeben werden"}), 500
        else:
            return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Bestelltes Gericht existiert nicht"}), 400
        
    ret_value = order_repo.create_order(jwt_userID, data_Orders)
    if ret_value=="created":
        return jsonify({api_message_descriptor:  f"{get_api_messages.SUCCESS.value}Bestellung erfolgreich"}), 201
    else:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Bestellung fehlgeschlagen"}), 500

@app.route('/orders_by_user/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check(user_repo)
def orders_by_user(start_date, end_date):
    jwt_userID = get_jwt_identity()
    orders = order_repo.get_orders_by_userid(jwt_userID, start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Sie haben keine Bestellungen in diesem Zeitraum"}), 404
 
@app.route('/orders_sorted_by_dish/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check(user_repo)
def orders_sorted_by_dish(start_date, end_date):
    orders = order_repo.get_orders_sorted_by_dish(start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Es gibt keine Bestellungen in diesem Zeitraum"}), 404
  
# -------------------------- Meal plan routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/create_meal_plan', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_meal_plan():
    data = request.json
    meal_plan = data.get('mealPlan') 
    if not meal_plan:
        return jsonify({api_message_descriptor: f"{get_api_messages.ERROR.value}Keine Speisepläne im JSON gefunden"}), 400

    for meal in meal_plan:
        dishID = meal.get('dishID')
        date = meal.get('date')
        if not (dishID and date):
            return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400
    
    ret_value = meal_plan_repo.create_mealPlan(meal_plan)
    if ret_value[0]:
        if ret_value[1] == '':
            return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Speiseplan erfolgreich erstellt"}), 201
        else:
            return jsonify({api_message_descriptor:  f"{get_api_messages.WARNING.value}Speiseplan erfolgreich erstellt, {ret_value[1]} sind bereits vorhanden"}), 201
    else:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}{str(ret_value[1])}"}),420 

@app.route('/meal_plan/<string:start_date>/<string:end_date>')
def meal_plan(start_date, end_date):
    if not (start_date and end_date):
            return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400
    meal_Plan = meal_plan_repo.get_mealPlan(start_date, end_date)
    if meal_Plan[0]:
        return jsonify(meal_Plan[1]), 201
    elif meal_Plan[0]== None:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}Kein Speiseplan im gewählten Zeitraum gefunden"}), 404
    else:
        return jsonify({api_message_descriptor:  f"{get_api_messages.ERROR.value}{str(meal_Plan[1])}"}),420

# -------------------------- Other Routes  ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/get_this_week')
def get_this_week():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return  jsonify({"monday": monday.strftime("%Y-%m-%d"), "sunday": sunday.strftime("%Y-%m-%d")}), 201

@app.route('/get_next_week')
def get_next_week():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday()) + timedelta(days=7)
    sunday = monday + timedelta(days=6)
    return  jsonify({"monday": monday.strftime("%Y-%m-%d"), "sunday": sunday.strftime("%Y-%m-%d")}), 201




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
