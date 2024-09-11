import pytest
import base64
from DB_Repositories.models import Allergy, User
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR
from flask_jwt_extended import decode_token, create_access_token
from datetime import timedelta

@pytest.mark.usefixtures("session")

########################################################## login test ##########################################################

def test_login_succes_admin_role(app, client, session):
    """Test login with admin role."""
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
    """Test login with kantinenmitarbeiter role."""
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
    """Test login with hungernde role."""
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
    
def test_login_missing_json(client):
    """Test login with missing json."""
    loginData= None
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fehlendes JSON in der Anfrage"
    
def test_login_missing_fields(client):
    """Test login with missing fields"""
    loginData= {
    "email": None,
    "password": None
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fehlender Benutzername oder Passwort"
    
def test_login_invalid_login_data(client):
    """Test login with invalid login"""
    loginData= {
    "email": "admin@test.com",
    "password": "wrong"
    }
    response = client.post('/login',
                            json=loginData)
    
    assert response.status_code == 401
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Falscher Benutzername oder Passwort"
    
########################################################## create_user test ##########################################################

def test_create_user_success(client, session, delete_all_users):
    """Test creating a user"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
            
def test_create_user_missing_allergies(client, session, delete_all_users):
    """Test creating a user with missing allergies"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Benutzer erfolgreich erstellt, aber die folgenden Allergien ['TestAllergyThree'] sind nicht in der Datenbank vorhanden"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
def test_create_user_already_exists(client, session, delete_all_users):
    """Test creating a user that already exists"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    responseTwo = client.post('/create_user',
                           json=data
                           )
    
    assert responseTwo.status_code == 500
    assert responseTwo.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Benutzer mit der E-Mail {data['email']} exisitiert bereits"
    
def test_create_user_missing_fields(client, delete_all_users):
    """Test creating a user with missing fields"""
    # Post-Data
    data = {
        'email': None,
        'password': None,
        'lastName': None,
        'firstName': None,
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"
    
########################################################## create_user_as_admin test ##########################################################

def test_create_user_as_admin_success_role_admin(client, auth_token_admin, session, delete_all_users):
    """Test creating a user as admin"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'admin',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    print (auth_token_admin)
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    assert user.role == data["role"]
    
def test_create_user_as_admin_success_role_kantinenmitarbeiter(client, auth_token_admin, session, delete_all_users):
    """Test creating a user as admin"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'kantinenmitarbeiter',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    print (auth_token_admin)
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    assert user.role == data["role"]
    
def test_create_user_as_admin_success_role_hungernde(client, auth_token_admin, session, delete_all_users):
    """Test creating a user as admin"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'hungernde',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    print (auth_token_admin)
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    assert user.role == data["role"]

def test_create_user_as_admin_missing_fields(client, delete_all_users, auth_token_admin):
    """Test creating a user as admin with missing fields"""
    # Post-Data
    data = {
        'email': None,
        'password': None,
        'lastName': None,
        'firstName': None,
        'role': None,
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"
    
def test_create_user_as_admin_missing_allergies(client, session, delete_all_users, auth_token_admin):
    """Test creating a user as admin with missing allergies"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'admin',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Benutzer erfolgreich erstellt, aber die folgenden Allergien ['TestAllergyThree'] sind nicht in der Datenbank vorhanden"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]

def test_create_user_as_admin_already_exists(client, session, delete_all_users, auth_token_admin):
    """Test creating a user that already exists"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'admin',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if dish suggestion was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    responseTwo = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responseTwo.status_code == 500
    assert responseTwo.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Benutzer mit der E-Mail {data['email']} exisitiert bereits"
    
def test_create_user_as_admin_invalid_role(client, delete_all_users, auth_token_admin):
    """Test creating a user as admin with missing allergies"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'test',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Die Rolle {data['role']} , existiert nicht"

########################################################## all_users test ##########################################################

def test_all_users_succes(client, auth_token_admin, delete_all_users):
    response = client.get(f'/all_users',
                          headers={'Authorization': f'Bearer {auth_token_admin}'}
                          )

    assert response.status_code == 200
    assert response.json == [{'allergies': None, 'email': 'admin@test.com', 'firstName': 'test', 'lastName': 'admin', 'role': 'admin', 'userID': 1}, {'allergies': None, 'email': 'kantinenmitarbeiter@test.com', 'firstName': 'test', 'lastName': 'kantinenmitarbeiter', 'role': 'kantinenmitarbeiter', 'userID': 2}, {'allergies': None, 'email': 'hungernder@test.com', 'firstName': 'test', 'lastName': 'hungernder', 'role': 'hungernde', 'userID': 3}]
    
########################################################## user_by_id test ##########################################################

def test_user_by_id_succes(client, auth_token_admin):
    response = client.get(f'/user_by_id/1',
                          headers={'Authorization': f'Bearer {auth_token_admin}'}
                          )
    
    assert response.status_code == 200
    assert response.json == {'allergies': None, 'email': 'admin@test.com', 'firstName': 'test', 'lastName': 'admin', 'role': 'admin', 'userID': 1}
    
def test_user_by_id_not_founde(client, auth_token_admin, delete_all_users):
    response = client.get(f'/user_by_id/4',
                          headers={'Authorization': f'Bearer {auth_token_admin}'}
                          )
    
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"
    
########################################################## allergy_by_userid test ##########################################################

def test_allergy_by_userid_succes_admin(client, auth_token_admin, session, delete_all_users):
    """Test allergy by userid as admin"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    responseTwo = client.get(f'/allergy_by_userid/{user.userID}',
                            headers={'Authorization': f'Bearer {auth_token_admin}'}
                            )
    
    assert responseTwo.status_code == 200
    assert responseTwo.json == data['allergies']
    
def test_allergy_by_userid_succes_hungernder(client, auth_token_hungernde, session, delete_all_users):
    """Test allergy by userid as hungernder"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    responseTwo = client.get(f'/allergy_by_userid/{user.userID}',
                            headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                            )
    
    assert responseTwo.status_code == 200
    assert responseTwo.json == data['allergies']
    
def test_allergy_by_userid_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, session, delete_all_users):
    """Test allergy by userid as hungernder"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    responseTwo = client.get(f'/allergy_by_userid/{user.userID}',
                            headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'}
                            )
    
    assert responseTwo.status_code == 403
    assert responseTwo.json[f'API_MESSAGE_DESCRIPTOR'] == f"Zugriff nicht gestattet! allergy_by_userid Berechtigung erforderlich"
    
def test_allergy_by_userid_no_allergies_found(client, auth_token_admin, session, delete_all_users):
    """Test allergy by userid with no allergies found"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': None
    }
    response = client.post('/create_user',
                           json=data
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    responseTwo = client.get(f'/allergy_by_userid/{user.userID}',
                            headers={'Authorization': f'Bearer {auth_token_admin}'}
                            )
    
    assert responseTwo.status_code == 404
    assert responseTwo.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Keine Allergien für diesen Benutzer hinterlegt"
    
def test_allergy_by_userid_user_not_found(client, auth_token_admin, delete_all_users):
    """Test allergy by userid but no user was found"""
        
    responseTwo = client.get('/allergy_by_userid/4',
                            headers={'Authorization': f'Bearer {auth_token_admin}'}
                            )
    
    assert responseTwo.status_code == 404
    assert responseTwo.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Benutzer nicht gefunden"
    
########################################################## set_user_allergies test ##########################################################

def test_set_user_allergies_succes_hungernde(app, client, session, delete_all_users):
    """Test set user allergies as hungernde"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': None
    }
    response = client.post('/create_user',
                           json=data,
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    loginData= {
    "email": data['email'],
    "password": data['password']
    }
    responseTwo = client.post('/login',
                            json=loginData)
    
    assert responseTwo.status_code == 200
    user = session.query(User).filter(User.email == loginData["email"]).first()

    access_token = responseTwo.json.get("access_token")
    assert access_token is not None
    with app.app_context():
        decoded_token = decode_token(access_token)
    
    assert decoded_token["sub"] == user.userID
    assert responseTwo.json["access_token"] == access_token
    assert responseTwo.json["userID"] == user.userID
    assert responseTwo.json["role"] == user.role
    
    with app.app_context():
        generated_token = create_access_token(identity=user.userID, expires_delta=timedelta(hours=1))
        
    dataTwo = {
    'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }

    responseThree = client.post('/set_user_allergies',
                                json = dataTwo,
                                headers={'Authorization': f'Bearer {generated_token}'}
                                )
    
    assert responseThree.status_code == 201
    assert responseThree.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Allergien erfolgreich angepasst"
    
def test_set_user_allergies_succes_admin(app, client, session, delete_all_users, auth_token_admin):
    """Test set user allergies as admin"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'role': 'admin',
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_user_as_admin',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    print (auth_token_admin)
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    assert user.role == data["role"]
    
    loginData= {
    "email": data['email'],
    "password": data['password']
    }
    responseTwo = client.post('/login',
                            json=loginData)
    
    assert responseTwo.status_code == 200
    user = session.query(User).filter(User.email == loginData["email"]).first()

    access_token = responseTwo.json.get("access_token")
    assert access_token is not None
    with app.app_context():
        decoded_token = decode_token(access_token)
    
    assert decoded_token["sub"] == user.userID
    assert responseTwo.json["access_token"] == access_token
    assert responseTwo.json["userID"] == user.userID
    assert responseTwo.json["role"] == user.role
    
    with app.app_context():
        generated_token = create_access_token(identity=user.userID, expires_delta=timedelta(hours=1))
        
    dataTwo = {
    'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }

    responseThree = client.post('/set_user_allergies',
                                json = dataTwo,
                                headers={'Authorization': f'Bearer {generated_token}'}
                                )
    
    assert responseThree.status_code == 201
    assert responseThree.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Allergien erfolgreich angepasst"
    
def test_set_user_allergies_allergies_not_found(app, client, session, delete_all_users):
    """Test set user allergies with unknown allergies"""
    # Post-Data
    data = {
        'email': 'test@test.com',
        'password': 'test',
        'lastName': 'lastname',
        'firstName': 'firstname',
        'allergies': None
    }
    response = client.post('/create_user',
                           json=data,
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Benutzer erfolgreich erstellt"
    
    # check if user was created
    user = session.query(User).filter_by(email = data["email"]).first()
    assert user is not None
    assert user.lastName == data["lastName"]
    assert user.firstName == data["firstName"]
    
    loginData= {
    "email": data['email'],
    "password": data['password']
    }
    responseTwo = client.post('/login',
                            json=loginData)
    
    assert responseTwo.status_code == 200
    user = session.query(User).filter(User.email == loginData["email"]).first()

    access_token = responseTwo.json.get("access_token")
    assert access_token is not None
    with app.app_context():
        decoded_token = decode_token(access_token)
    
    assert decoded_token["sub"] == user.userID
    assert responseTwo.json["access_token"] == access_token
    assert responseTwo.json["userID"] == user.userID
    assert responseTwo.json["role"] == user.role
    
    with app.app_context():
        generated_token = create_access_token(identity=user.userID, expires_delta=timedelta(hours=1))
        
    dataTwo = {
    'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
    }

    responseThree = client.post('/set_user_allergies',
                                json = dataTwo,
                                headers={'Authorization': f'Bearer {generated_token}'}
                                )
    
    assert responseThree.status_code == 201
    assert responseThree.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Allergien erfolgreich angepasst, aber die folgenden Allergien ['TestAllergyThree'] sind nicht in der Datenbank vorhanden"
