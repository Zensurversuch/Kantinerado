import pytest
import base64
from DB_Repositories.models import Allergy, User
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from flask_jwt_extended import decode_token
from datetime import timedelta

@pytest.mark.usefixtures("session")

########################################################## login test ##########################################################
def test_login_succes_admin_role(app, client, session):
    loginData= {
    "email": "admin@test.com",
    "password": "admin_test"
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 200
    user = session.query(User).filter(User.email == loginData["email"]).first()
    
    access_token = response.json.get("access_token")
    assert access_token is not None
    with app.app_context():
        decoded_token = decode_token(access_token)
    
    assert decoded_token["sub"] == user.userID
    assert response.json["access_token"] == access_token
    assert response.json["userID"] == user.userID
    assert response.json["role"] == user.role 
    
def test_login_succes_kantinenmitarbeiter_role(app, client, session):
    loginData= {
    "email": "kantinenmitarbeiter@test.com",
    "password": "kantinenmitarbeiter_test"
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 200
    user = session.query(User).filter(User.email == loginData["email"]).first()
    
    access_token = response.json.get("access_token")
    assert access_token is not None
    with app.app_context():
        decoded_token = decode_token(access_token)
    
    assert decoded_token["sub"] == user.userID
    assert response.json["access_token"] == access_token
    assert response.json["userID"] == user.userID
    assert response.json["role"] == user.role 
    
def test_login_succes_hungernde_role(app, client, session):
    loginData= {
    "email": "hungernder@test.com",
    "password": "hungernder_test"
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 200
    user = session.query(User).filter(User.email == loginData["email"]).first()
    
    access_token = response.json.get("access_token")
    assert access_token is not None
    with app.app_context():
        decoded_token = decode_token(access_token)
    
    assert decoded_token["sub"] == user.userID
    assert response.json["access_token"] == access_token
    assert response.json["userID"] == user.userID
    assert response.json["role"] == user.role
    
def test_login_missing_json(app, client, session):
    loginData= None
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fehlendes JSON in der Anfrage"
    
def test_login_missing_fields(app, client, session):
    loginData= {
    "email": None,
    "password": None
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fehlender Benutzername oder Passwort"
    
def test_login_invalid_login_data(app, client, session):
    loginData= {
    "email": "admin@test.com",
    "password": "wrong"
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 401
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Falscher Benutzername oder Passwort"