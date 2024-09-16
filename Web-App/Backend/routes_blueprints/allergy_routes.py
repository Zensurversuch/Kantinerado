from flask import Blueprint, jsonify, current_app
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

allergy_blueprint = Blueprint('allergy_blueprint', __name__)
@allergy_blueprint.route('/all_allergies')
def all_allergies():
    data = current_app.allergy_repo.get_all_allergies()
    if data:
        return jsonify(data)
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Keine Allergien gefunden"}), 404