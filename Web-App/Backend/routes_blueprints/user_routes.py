from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from decorators import permission_check
import hashlib
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from config import user_repo

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fehlendes JSON in der Anfrage"}), 400

    data_email = request.json.get('email', None)
    data_password = request.json.get('password', None)
   

    if not data_email or not data_password:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fehlender Benutzername oder Passwort"}), 400

    
    user_data = user_repo.get_user_by_email(data_email)

    if user_data:
        hashed_pw = hashlib.sha256((data_password + user_data["salt"]).encode('utf-8')).hexdigest()
        if (hashed_pw == user_data["password"]):
            access_token = create_access_token(identity=user_data["userID"], expires_delta=timedelta(hours=1))
            return jsonify(access_token=access_token, userID = user_data["userID"], role = user_data["role"]), 200
        
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Falscher Benutzername oder Passwort"}), 401

@user_blueprint.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    data_email = data.get('email')
    data_password = data.get('password')
    data_lastName = data.get('lastName')
    data_firstName = data.get('firstName')
    data_allergies = data.get('allergies')
    if not (data_email and data_password and data_lastName and data_firstName):
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    if user_repo.get_user_by_email(data_email):
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Benutzer mit der E-Mail {data_email} exisitiert bereits"}), 500

    ret_value = user_repo.create_user(data_email, data_password, data_lastName, data_firstName, "hungernde", data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.WARNING.value}Benutzer erfolgreich erstellt, aber die folgenden Allergien {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Benutzer konnte nicht erstellt werden"}), 500

@user_blueprint.route('/create_user_as_admin', methods=['POST'])
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
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"}), 400

    if data_role not in ["hungernde", "admin", "kantinenmitarbeiter"]:
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value} Die Rolle {data_role} , existiert nicht"}), 400

    if user_repo.get_user_by_email(data_email):
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Benutzer mit der E-Mail {data_email} exisitiert bereits"}), 500

    ret_value = user_repo.create_user(data_email, data_password, data_lastName, data_firstName, data_role, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.WARNING.value}Benutzer erfolgreich erstellt, aber die folgenden Allergien {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Benutzer konnte nicht erstellt werden"}), 500

@user_blueprint.route('/all_users')
@jwt_required()
@permission_check(user_repo)
def all_users():
    data = user_repo.get_all_users()
    if data:
        return jsonify(data)
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404

@user_blueprint.route('/user_by_id/<int:user_id>')
@jwt_required()
@permission_check(user_repo)
def user_by_id(user_id):
    user = user_repo.get_user_by_id(user_id)
    if user:
        return user
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404

@user_blueprint.route('/user_by_email/<string:email>')
@jwt_required()
@permission_check(user_repo)
def user_by_email(email):
    user = user_repo.get_user_by_email(email)
    if user:
        return user
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404

@user_blueprint.route('/allergy_by_userid/<int:user_id>')
@jwt_required()
@permission_check(user_repo)
def allergy_by_userid(user_id):
    user_data = user_repo.get_user_by_id(user_id)
    if user_data:
        if user_data["allergies"] != None:
            return user_data["allergies"]  
        else:
            return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.WARNING.value}Keine Allergien für diesen Benutzer hinterlegt"}), 404
    return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404


@user_blueprint.route('/set_user_allergies',  methods=['POST'])
@jwt_required()
@permission_check(user_repo)
def set_user_allergies():
    data = request.json
    jwt_userID = get_jwt_identity()
    data_allergies = data.get('allergies')
    ret_value = user_repo.set_user_allergies_by_id(jwt_userID, data_allergies)
    if ret_value == []:   # If ret_value is empty no allergies were missing
        return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.SUCCESS.value}Allergien erfolgreich angepasst"}), 201
    elif ret_value:     # If ret_value contains values allergies were missing or the user wasn't found
        if ret_value == "User not found!":
            return jsonify({API_MESSAGE_DESCRIPTOR:  f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"}), 404
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.WARNING.value}Allergien erfolgreich angepasst, aber die folgenden Allergien {ret_value} sind nicht in der Datenbank vorhanden"}), 201
    elif ret_value == False:
        return jsonify({API_MESSAGE_DESCRIPTOR: f"{get_api_messages.ERROR.value}Allergien konnten nicht angepasst werden"}), 500
