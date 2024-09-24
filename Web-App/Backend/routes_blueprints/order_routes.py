from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from decorators import permission_check
from datetime import datetime, timedelta


order_blueprint = Blueprint('order_blueprint', __name__)

@order_blueprint.route('/create_order', methods=['POST'])
@jwt_required()
@permission_check()
def create_order():
    data = request.json
    jwt_userID = get_jwt_identity()
    data_Orders = data.get('orders')
    mealPlan_ids = []

    if not data_Orders:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Keine Bestellungen im JSON gefunden"}), 400

    for order in data_Orders:
        mealPlanID = order.get('mealPlanID')
        amount = order.get('amount')
        if (mealPlanID == None and amount == None):
            return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400
        mealPlan_ids.append(mealPlanID)

    timestamp = datetime.today()
    mealPlanDates = current_app.meal_plan_repo.get_mealPlan_dates_by_ids(mealPlan_ids)
    if mealPlanDates:
        monday = timestamp - timedelta(days=timestamp.weekday())
        sunday = monday + timedelta(days=6) 
        if any(datetime.strptime(mealPlanDate, "%Y-%m-%d") < sunday for mealPlanDate in mealPlanDates): 
                return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Es können keine Bestellungen mehr für die aktuelle und vergangenen Wochen aufgegeben werden"}), 400
        if (timestamp.weekday() == 3 and timestamp.hour >= 18) or (timestamp.weekday() > 3):
            next_monday = timestamp - timedelta(days=timestamp.weekday()) + timedelta(days=7)
            next_sunday = next_monday + timedelta(days=6)
            if any(datetime.strptime(mealPlanDate, "%Y-%m-%d") < next_sunday for mealPlanDate in mealPlanDates): 
                return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Es können keine Bestellungen mehr nach Donnerstag 16 Uhr für nächste Woche aufgegeben werden"}), 400
    else:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Bestelltes Gericht existiert nicht"}), 400

    ret_value = current_app.order_repo.create_order(jwt_userID, data_Orders)
    if ret_value=="created":
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Bestellung erfolgreich"}), 201
    else:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Bestellung fehlgeschlagen"}), 400

@order_blueprint.route('/orders_by_user/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check()
def orders_by_user(start_date, end_date):
    jwt_userID = get_jwt_identity()
    orders = current_app.order_repo.get_orders_by_userid(jwt_userID, start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Sie haben keine Bestellungen in diesem Zeitraum"}), 400
 
@order_blueprint.route('/orders_sorted_by_dish/<string:start_date>/<string:end_date>')
@jwt_required()
@permission_check()
def orders_sorted_by_dish(start_date, end_date):
    orders = current_app.order_repo.get_orders_sorted_by_dish(start_date, end_date)

    if orders:
        return jsonify(orders)
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Es gibt keine Bestellungen in diesem Zeitraum"}), 404
