from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from decorators import permission_check
import base64

dishSuggestion_blueprint = Blueprint('dishSuggestion_blueprint', __name__)

@dishSuggestion_blueprint.route('/create_dish_suggestion', methods=['POST'])
@jwt_required()
@permission_check()
def create_dish_suggestion():
    data = request.json
    data_name = data.get('name')
    data_ingredients = data.get('ingredients')
    data_image = data.get('image')

    if not (data_name):
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    decoded_image = base64.b64decode(data_image) if data_image else None

    ret_value = current_app.dish_suggestion_repo.create_dishSuggestion(data_name, data_ingredients, decoded_image,)
    if ret_value:  
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich erstellt"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gerichtsvorschlag konnte nicht erstellt werden"}), 500