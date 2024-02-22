from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from flasgger import Swagger
from role_permissions import get_permissions_for_role

testing = True

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  
jwt = JWTManager(app)
Swagger(app)

# Beispielbenutzerdaten mit Rolle -> Die Rolle muss später aus der Datenbank kommen
users = {
    'user1': {'password': 'password1', 'role': ['admin']},
    'user2': {'password': 'password2', 'role': ['user']}
}

@app.route('/login', methods=['POST'])
def login():
    """
    Benutzeranmelde-Endpunkt
    ---
    parameters:
      - name: username
        in: body
        type: string
        required: true
      - name: password
        in: body
        type: string
        required: true
    responses:
      200:
        description: Ein JWT-Token zur Authentifizierung
      400:
        description: Fehlende JSON-Anfrage oder fehlender Benutzername oder Passwort
      401:
        description: Falscher Benutzername oder Passwort
    """
    if not request.is_json:
        return jsonify({"msg": "Fehlendes JSON in der Anfrage"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Fehlender Benutzername oder Passwort"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Falscher Benutzername oder Passwort"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route("/hello")
#@swag_from('swagger/hello.yml')  # Spezifiziere die Swagger-YAML-Datei für diesen Endpunkt
def hello():
    """
    Hello-Endpunkt
    ---
    responses:
      200:
        description: Nachricht, wenn die Berechtigung gewährt ist
      403:
        description: Nachricht, wenn die Berechtigung erforderlich ist
    """
    if not testing:
        current_user = get_jwt_identity()
        current_role = "admin" #Hier muss die Rolle von der Datenbank kommen mithilfe des current_user-Namens
    else:
        current_user = "user1"
        current_role = "admin"
   
    current_permissions = set(get_permissions_for_role(current_role))
    if 'hello' in current_permissions:
        return jsonify(logged_in_as=current_user, message='Zugriff auf Geld gewährt! Hallo, Welt!')
    else:
        return jsonify(message='Zugriff mit Berechtigung für Geld erforderlich!'), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)