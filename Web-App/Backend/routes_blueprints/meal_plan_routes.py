from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from decorators import permission_check

meal_plan_blueprint = Blueprint('meal_plan_blueprint', __name__)

@meal_plan_blueprint.route('/create_meal_plan', methods=['POST'])
@jwt_required()
@permission_check()
def create_meal_plan():
    data = request.json
    meal_plan = data.get('mealPlan') 
    if not meal_plan:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Keine Speisepläne im JSON gefunden"}), 400

    for meal in meal_plan:
        dishID = meal.get('dishID')
        date = meal.get('date')
        if not (dishID and date):
            return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    ret_value = current_app.meal_plan_repo.create_mealPlan(meal_plan)
    if ret_value[0]:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Speiseplan erfolgreich erstellt"}), 201
    else:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}{str(ret_value[1])}"}),420 

@meal_plan_blueprint.route('/meal_plan/<string:start_date>/<string:end_date>')
def meal_plan(start_date, end_date):
    meal_Plan = current_app.meal_plan_repo.get_mealPlan(start_date, end_date)
    if meal_Plan[0]:
        return jsonify(meal_Plan[1]), 201
    elif meal_Plan[0]== None:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Kein Speiseplan im gewählten Zeitraum gefunden"}), 404
    else:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}{str(meal_Plan[1])}"}),420