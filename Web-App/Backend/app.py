from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import create_engine, MetaData
from DB_Repositories import userRepository, dishesRepository, orderRepository, mealPlanRepository, allergyRepository
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


# -------------------------- Client Routes ---------------------------------------------------------------------------------------------------------------------------------------
@app.route("/hello")
@jwt_required()
@permission_check(user_repo)
def hello():
    jwt_userID = get_jwt_identity()
    return jsonify(logged_in_as=jwt_userID, message='Zugriff auf Hello gestattet! Hallo, Welt!')



# -------------------------- User Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Fehlendes JSON in der Anfrage"}), 400

    data_email = request.json.get('email', None)
    data_password = request.json.get('password', None)
    hashed_pw = hashlib.sha256(data_password.encode('utf-8')).hexdigest()

    if not data_email or not data_password:
        return jsonify({"msg": "Fehlender Benutzername oder Passwort"}), 400

    user_data = user_repo.get_user_by_email(data_email)

    if user_data and (hashed_pw == user_data["password"]):
        access_token = create_access_token(identity=user_data["userID"], expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token, userID = user_data["userID"], role = user_data["role"]), 200
    else:
        return jsonify({"msg": "Falscher Benutzername oder Passwort"}), 401

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    data_email = data.get('email')
    data_password = data.get('password')
    data_lastName = data.get('lastName')
    data_firstName = data.get('firstName')
    data_allergies = data.get('allergies')
    if not (data_email and data_password and data_lastName and data_firstName):
        return jsonify({"message": "Missing required fields"}), 400

    if user_repo.get_user_by_email(data_email):
        return jsonify({"message": f"User with the email {data_email} already exists"}), 500

    ret_value = user_repo.create_user(data_email, data_password, data_lastName, data_firstName, "hungernde", data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
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
    data_email = data.get('email')
    data_password = data.get('password')
    data_lastName = data.get('lastName')
    data_firstName = data.get('firstName')
    data_role = data.get('role')
    data_allergies = data.get('allergies')
    if not (data_email and data_password and data_lastName and data_firstName and data_role):
        return jsonify({"message": "Missing required fields"}), 400

    if data_role not in ["hungernde", "admin", "kantinenmitarbeiter"]:
        return jsonify({"message": f"the role: {data_role} , doesn't exist"}), 400

    if user_repo.get_user_by_email(data_email):
        return jsonify({"message": f"User with the email {data_email} already exists"}), 500

    ret_value = user_repo.create_user(data_email, data_password, data_lastName, data_firstName, data_role, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
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

# -------------------------- Allergy Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/allergy_by_id/<int:allergy_id>')
def allergy_by_id(allergy_id):
    allergy = allergy_repo.get_allergie_by_id(allergy_id)
    if allergy:
        return allergy
    return jsonify({"message": "Allergy not found"}), 404

@app.route('/all_allergies')
def all_allergies():
    data = allergy_repo.get_all_allergies()
    if data:
        return jsonify(data)
    return jsonify({"message": "No allergies found"}), 404


# -------------------------- Dish Routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/dish_by_id/<int:dish_id>')
@jwt_required()
@permission_check(user_repo)
def dish_by_id(dish_id):
    dish = dish_repo.get_dish_by_id(dish_id)
    if dish:
        return dish
    return jsonify({"message": "Dish not found"}), 404

@app.route('/dish_by_name/<string:dish_name>')
@jwt_required()
@permission_check(user_repo)
def dish_by_name(dish_name):
    dish = dish_repo.get_dish_by_name(dish_name)
    if dish:
        return dish
    return jsonify({"message": "Dish not found"}), 404

@app.route('/dish_by_mealType/<string:dish_mealType>')
#@jwt_required()
#@permission_check(user_repo)
def dish_by_mealType(dish_mealType):
    dishes = dish_repo.get_dishes_by_mealType(dish_mealType)
    if dishes:
        return dishes
    return jsonify({"message": "No Dishes found"}), 404


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
        return jsonify({"message": "Missing required fields"}), 400

    if dish_repo.get_dish_by_name(data_name):
        return jsonify({"message": "Dish exist already"}), 400

    decoded_image = base64.b64decode(data_image) if data_image else None

    ret_value = dish_repo.create_dish(data_name, data_price, data_dietaryCategory, data_mealType, data_ingredients, decoded_image, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
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
    jwt_userID = get_jwt_identity()
    data_Orders = data.get('orders')
    mealPlan_ids = []

    if not data_Orders:
        return jsonify({"message": "No orders found in the request"}), 400

    for order in data_Orders:
        mealPlanID = order.get('mealPlanID')
        amount = order.get('amount')
        if not (mealPlanID and amount):
            return jsonify({"message": "Missing required fields"}), 400
        mealPlan_ids.append(mealPlanID)

    timestamp = datetime.today()
    if (timestamp.weekday() == 3 and timestamp.hour >= 18) or (timestamp.weekday() > 3):
        mealPlanDates = meal_plan_repo.get_mealPlan_dates_by_ids(mealPlan_ids)
        if mealPlanDates:
            monday = timestamp - timedelta(days=timestamp.weekday()) + timedelta(days=7)
            sunday = monday + timedelta(days=6)
            if any(datetime.strptime(mealPlanDate, "%Y-%m-%d") < sunday for mealPlanDate in mealPlanDates): 
                return jsonify({"message": "Cannot order after Thursday 6pm"}), 500
        else:
            return jsonify({"message": "Missing mealPlans in Database"}), 400
        
    ret_value = order_repo.create_order(jwt_userID, data_Orders)
    if ret_value=="created":
        return jsonify({"message": "Order created successful"}), 201
    else:
        return jsonify({"message": "Failed to create Order"}), 500

@app.route('/orders_by_user/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check(user_repo)
def orders_by_user(start_date, end_date):
    jwt_userID = get_jwt_identity()
    orders = order_repo.get_orders_by_userid(jwt_userID, start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({"message": "No orders for you found in the selected timespan"}), 404
 
@app.route('/orders_sorted_by_dish/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check(user_repo)
def orders_sorted_by_dish(start_date, end_date):
    orders = order_repo.get_orders_sorted_by_dish(start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({"message": "No orders for you found in the selected timespan"}), 404
  
# -------------------------- Meal plan routes ------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/create_meal_plan', methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def create_meal_plan():
    data = request.json
    meal_plan = data.get('mealPlan') 
    if not meal_plan:
        return jsonify({"message": "No meal plan found in the request"}), 400

    for meal in meal_plan:
        dishID = meal.get('dishID')
        date = meal.get('date')
        if not (dishID and date):
            return jsonify({"message": "Missing required fields"}), 400
    
    ret_value = meal_plan_repo.create_mealPlan(meal_plan)
    if ret_value[0]:
        if ret_value[1] == '':
            return jsonify({"message": "Meal plan processed successfully"}), 201
        else:
            return jsonify({"message": ret_value[1]}), 201
    else:
        return jsonify({"message":  str(ret_value[1])}),420 

@app.route('/meal_plan/<string:start_date>/<string:end_date>')
def meal_plan(start_date, end_date):
    if not (start_date and end_date):
            return jsonify({"message": "Missing required fields"}), 400
    meal_Plan = meal_plan_repo.get_mealPlan(start_date, end_date)
    if meal_Plan[0]:
        return jsonify(meal_Plan[1]), 201
    elif meal_Plan[0]== None:
        return jsonify({"message": "no mealplan found"})
    else:
        return jsonify({"message":  str(meal_Plan[1])}),420

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
