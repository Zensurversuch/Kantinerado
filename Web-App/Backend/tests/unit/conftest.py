import pytest
from unittest.mock import patch
from flask_jwt_extended import JWTManager
from __init__ import create_app

@pytest.fixture(scope='module')
def app():
    # Setze die Testkonfiguration für die Flask-Anwendung
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    # Verwende den Test-Client der Flask-Anwendung
    return app.test_client()

@pytest.fixture(scope='module')
def jwt(app):
    # Initialisiere JWT Manager
    return JWTManager(app)

@pytest.fixture
def mock_dish_suggestion_repo(app):
    with patch('routes_blueprints.dishSuggestion_routes.current_app.dish_suggestion_repo') as mock_repo:
        yield mock_repo

@pytest.fixture
def mock_jwt_required(app):
    with patch('flask_jwt_extended.jwt_required') as mock_jwt:
        mock_jwt.return_value = lambda x: x
        yield mock_jwt
        
@pytest.fixture
def mock_user_repo():
    with patch('routes_blueprints.user_blueprint') as mock_repo:
        yield mock_repo

@pytest.fixture
def mock_get_permissions_for_role():
    with patch('role_permissions.get_permissions_for_role') as mock_permissions:
        mock_permissions.return_value = ['create_dish_suggestion']
        yield mock_permissions