from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_claims
from role_permissions import get_permissions_for_role


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  
jwt = JWTManager(app)


# Example user data with role -> die Rolle muss dan später aus der Datenbank kommen
users = {
    'user1': {'password': 'password1', 'role': ['admin']},
    'user2': {'password': 'password2', 'role': ['user']}
}


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, additional_claims={'role': users[username]['role']})
    return jsonify(access_token=access_token), 200



#Beispiel für permission check die permission muss in der Role Permission datei hinterlegt werden
@app.route("/hello")
def hello():
    current_user = get_jwt_identity()
    current_role = get_jwt_claims()['roles']
    current_permissions = set(get_permissions_for_role(current_role))
    if 'hello' in current_permissions:
        return jsonify(logged_in_as=current_user, message='Admin access to money granted! Hello, World!')
    else:
        return jsonify(message='Admin access with permission to money required!'), 403


if __name__ == "__main__":
    app.run(host='0.0.0.0')