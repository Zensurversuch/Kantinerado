from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from decorators import permission_check
import base64

dish_suggestion_blueprint = Blueprint('dishSuggestion_blueprint', __name__)

@dish_suggestion_blueprint.route('/create_dish_suggestion', methods=['POST'])
@jwt_required()
@permission_check()
def create_dish_suggestion():
    data = request.json
    data_name = data.get('name')
    data_ingredients = data.get('ingredients')
    data_image = data.get('image')
    data_description = data.get('description')
    if not (data_name):
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    decoded_image = base64.b64decode(data_image) if data_image else None

    ret_value = current_app.dish_suggestion_repo.create_dish_suggestion(data_name, data_ingredients, decoded_image, data_description)
    if ret_value:  
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich erstellt"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gerichtsvorschlag konnte nicht erstellt werden"}), 500

@dish_suggestion_blueprint.route('/all_dish_suggestions', methods=['GET'])
@jwt_required()
@permission_check()
def all_dish_suggestions():
    data = current_app.dish_suggestion_repo.all_dish_suggestions()
    if data:
        return jsonify(data)
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Keinen Gerichtsvorschlag gefunden"}), 404

@dish_suggestion_blueprint.route('/delete_dish_suggestion/<int:dishSuggestion_ID>')
@jwt_required()
@permission_check()
def delete_dish_suggestion(dishSuggestion_ID):
    ret_value = current_app.dish_suggestion_repo.delete_dish_suggestion(dishSuggestion_ID)
    if ret_value:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich gelöscht"}), 201
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gerichtsvorschlag nicht gefunden"}), 404

@dish_suggestion_blueprint.route('/accept_dish_suggestion', methods=['POST'])
@jwt_required()
@permission_check()
def accept_dish_suggestion():
    data = request.json
    data_dishSuggestionID = data.get('dishSuggestionID')

    dish_data = data.get('dishData', {})
    data_name = dish_data.get('name')
    data_price = dish_data.get('price')
    data_ingredients = dish_data.get('ingredients')
    data_dietaryCategory = dish_data.get('dietaryCategory')
    data_mealType = dish_data.get('mealType')
    data_image = dish_data.get('image')
    data_allergies = dish_data.get('allergies')

    if not (data_name and data_price and data_dietaryCategory and data_mealType and data_dishSuggestionID):
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderlichen Felder aus"}), 400

    if current_app.dish_repo.get_dish_by_name(data_name):
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Gericht existiert bereits"}), 400

    decoded_image = base64.b64decode(data_image) if data_image else None

    ret_value = current_app.dish_repo.create_dish(data_name, data_price, data_dietaryCategory, data_mealType, data_ingredients, decoded_image, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        ret_value_delete = current_app.dish_suggestion_repo.delete_dish_suggestion(data_dishSuggestionID)
        if ret_value_delete:
            return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt. Gerichtsvorschlag erfolgreich gelöscht"}), 201
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt. Gerichtsvorschlag konnte nicht gelöscht werden"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        ret_value_delete = current_app.dish_suggestion_repo.delete_dish_suggestion(data_dishSuggestionID)
        if ret_value_delete:
            return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allergie {ret_value} sind nicht in der Datenbank vorhanden Gerichtsvorschlag erfolgreich gelöscht"}), 201
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allergie {ret_value} sind nicht in der Datenbank vorhanden Gerichtsvorschlag konnte nicht gelöscht werden"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Gericht konnte nicht erstellt werden"}), 500