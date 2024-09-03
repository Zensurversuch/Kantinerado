import pytest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from ../decorators import permission_check
from role_permissions import UserRole

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'testsecret'
    jwt = JWTManager(app)
    
    # Dummy user repository
    class UserRepository:
        def __init__(self, users):
            self.users = users

        def get_user_by_id(self, user_id):
            return self.users.get(user_id)
    
    users = {
        1: {"id": 1, "role": UserRole.ADMIN.value},
        2: {"id": 2, "role": UserRole.HUNGERNDE.value},
        3: {"id": 3, "role": UserRole.KANTINENMITARBEITER.value},
    }

    user_repo = UserRepository(users)

    @app.route('/create_dish', methods=['POST'])
    @permission_check(user_repo)
    def create_dish():
        return jsonify({"msg": "Dish created!"}), 200

    @app.route('/all_users', methods=['GET'])
    @permission_check(user_repo)
    def all_users():
        return jsonify({"msg": "All users listed!"}), 200

    return app

def test_admin_can_access_all_users(app):
    with app.test_client() as client:
        access_token = create_access_token(identity=1)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.get('/all_users', headers=headers)
        assert response.status_code == 200
        assert response.json == {"msg": "All users listed!"}

def test_hungernde_cannot_access_create_dish(app):
    with app.test_client() as client:
        access_token = create_access_token(identity=2)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.post('/create_dish', headers=headers)
        assert response.status_code == 403
        assert "Zugriff nicht gestattet" in response.json['message']

def test_kantinenmitarbeiter_can_create_dish(app):
    with app.test_client() as client:
        access_token = create_access_token(identity=3)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.post('/create_dish', headers=headers)
        assert response.status_code == 200
        assert response.json == {"msg": "Dish created!"}
        
def test_hungernde_cannot_access_all_users(app):
    with app.test_client() as client:
        access_token = create_access_token(identity=2)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.get('/all_users', headers=headers)
        assert response.status_code == 403
        assert "Zugriff nicht gestattet" in response.json['message']

def test_kantinenmitarbeiter_cannot_access_all_users(app):
    with app.test_client() as client:
        access_token = create_access_token(identity=3)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = client.get('/all_users', headers=headers)
        assert response.status_code == 403
        assert "Zugriff nicht gestattet" in response.json['message']

