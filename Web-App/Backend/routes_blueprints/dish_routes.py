from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from config import user_repo, dish_repo
from decorators import permission_check
import base64


dish_blueprint = Blueprint('dish_blueprint', __name__)

@dish_blueprint.route('/dish_by_id/<int:dish_id>')
@jwt_required()
@permission_check(user_repo)
def dish_by_id(dish_id):
    dish = dish_repo.get_dish_by_id(dish_id)
    if dish:
        return dish
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gericht nicht gefunden"}), 404

@dish_blueprint.route('/dish_by_name/<string:dish_name>')
@jwt_required()
@permission_check(user_repo)
def dish_by_name(dish_name):
    dish = dish_repo.get_dish_by_name(dish_name)
    if dish:
        return dish
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gericht nicht gefunden"}), 404

@dish_blueprint.route('/dish_by_mealType/<string:dish_mealType>')
@jwt_required()
@permission_check(user_repo)
def dish_by_mealType(dish_mealType):
    dishes = dish_repo.get_dishes_by_mealType(dish_mealType)
    if dishes:
        return dishes
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Keine Gerichte gefunden"}), 404


@dish_blueprint.route('/create_dish', methods=['POST'])
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
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    if dish_repo.get_dish_by_name(data_name):
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Gericht existiert bereits"}), 400

    decoded_image = base64.b64decode(data_image) if data_image else None

    ret_value = dish_repo.create_dish(data_name, data_price, data_dietaryCategory, data_mealType, data_ingredients, decoded_image, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allerigie {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gericht konnte nicht erstellt werden"}), 500
