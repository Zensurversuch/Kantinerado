from flask import Blueprint, jsonify, request
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from config import allergy_repo

allergy_blueprint = Blueprint('allergy_blueprint', __name__)

@allergy_blueprint.route('/allergy_by_id/<int:allergy_id>')
def allergy_by_id(allergy_id):
    allergy = allergy_repo.get_allergie_by_id(allergy_id)
    if allergy:
        return allergy
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Allergie nicht gefunden"}), 404

@allergy_blueprint.route('/all_allergies')
def all_allergies():
    data = allergy_repo.get_all_allergies()
    if data:
        return jsonify(data)
    return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Keine Allergien gefunden"}), 404