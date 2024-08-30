import pytest
import base64
from DB_Repositories.models import DishSuggestion
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")
def test_create_dish_suggestion_succes_admin(client, auth_token_admin, session, delete_all_dish_suggestions):
    """Test creating a dish suggestionas admin."""
    # Post-Daten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    response = client.post('/create_dish_suggestion',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich erstellt"
    
    # Überprüfe, ob der Dish-Vorschlag tatsächlich erstellt wurde
    suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    assert suggestion is not None
    assert suggestion.name == 'Test Dish'
    
    if suggestion:
            session.delete(suggestion)
            session.commit()
            
def test_create_dish_suggestion_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, session, delete_all_dish_suggestions):
    """Test creating a dish suggestion as kantinenmitarbeiter."""
    # Post-Daten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    response = client.post('/create_dish_suggestion',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'}
                           )
    
    assert response.status_code == 403
    assert response.json['message'] == f"Zugriff nicht gestattet! create_dish_suggestion Berechtigung erforderlich"
    
    # Überprüfe, ob der Dish-Vorschlag tatsächlich erstellt wurde
    suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    assert suggestion is None
    
    if suggestion:
            session.delete(suggestion)
            session.commit()
                      
def test_create_dish_suggestion_succes_hungernde(client, auth_token_hungernde, session, delete_all_dish_suggestions):
    """Test creating a dish suggestion as Hungernder"""
    # Post-Daten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    response = client.post('/create_dish_suggestion',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich erstellt"
    
    # Überprüfe, ob der Dish-Vorschlag tatsächlich erstellt wurde
    suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    assert suggestion is not None
    assert suggestion.name == 'Test Dish'
    
    if suggestion:
            session.delete(suggestion)
            session.commit()
            
def test_create_dish_suggestion_missing_name(client, auth_token_hungernde, delete_all_dish_suggestions):
    # Testdaten ohne Namen
    data = {
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response = client.post('/create_dish_suggestion',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )

    # Überprüfe die Antwort
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"

def test_all_dish_suggestions_succes_kantinenarbeiter(client, auth_token_kantinenmitarbeiter, auth_token_hungernde, session, delete_all_dish_suggestions):
    dataOne = {
        'name': 'Test Dish One',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    
    dataTwo = {
        'name': 'Test Dish Two',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    responseOne = client.post('/create_dish_suggestion',
                json=dataOne,
                headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                )
    
    responseTwo = client.post('/create_dish_suggestion',
                json=dataTwo,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                )
    
    assert responseOne.status_code == 201
    assert responseTwo.status_code == 201
    
    response = client.get('/all_dish_suggestions',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    # Überprüfen der JSON-Antwort
    response_data = response.get_json()
    print (response_data)
    assert response_data is not None
    assert len(response_data) >= 2  # Es sollten mindestens 2 Gerichtsvorschläge vorhanden sein

    # Überprüfen, ob die Testdaten in der Antwort enthalten sind
    dish_names = [dish['name'] for dish in response_data]
    assert dataOne['name'] in dish_names
    assert dataTwo['name'] in dish_names

    # Teardown: Entferne die hinzugefügten Datensätze aus der Datenbank
    dish_suggestion_one = session.query(DishSuggestion).filter_by(name=dataOne['name']).first()
    dish_suggestion_two = session.query(DishSuggestion).filter_by(name=dataTwo['name']).first()
    
    if dish_suggestion_one:
        session.delete(dish_suggestion_one)
    if dish_suggestion_two:
        session.delete(dish_suggestion_two)
    session.commit()
    
def test_all_dish_suggestions_succes_admin(client, auth_token_admin, auth_token_hungernde, session, delete_all_dish_suggestions):
    dataOne = {
        'name': 'Test Dish One',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    
    dataTwo = {
        'name': 'Test Dish Two',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    responseOne = client.post('/create_dish_suggestion',
                json=dataOne,
                headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                )
    
    responseTwo = client.post('/create_dish_suggestion',
                json=dataTwo,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                )
    
    assert responseOne.status_code == 201
    assert responseTwo.status_code == 201
    
    response = client.get('/all_dish_suggestions',
                          headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    # Überprüfen der JSON-Antwort
    response_data = response.get_json()
    print (response_data)
    assert response_data is not None
    assert len(response_data) >= 2  # Es sollten mindestens 2 Gerichtsvorschläge vorhanden sein

    # Überprüfen, ob die Testdaten in der Antwort enthalten sind
    dish_names = [dish['name'] for dish in response_data]
    assert dataOne['name'] in dish_names
    assert dataTwo['name'] in dish_names

    # Teardown: Entferne die hinzugefügten Datensätze aus der Datenbank
    dish_suggestion_one = session.query(DishSuggestion).filter_by(name=dataOne['name']).first()
    dish_suggestion_two = session.query(DishSuggestion).filter_by(name=dataTwo['name']).first()
    
    if dish_suggestion_one:
        session.delete(dish_suggestion_one)
    if dish_suggestion_two:
        session.delete(dish_suggestion_two)
    session.commit()

def test_all_dish_suggestions_hungernde(client, auth_token_hungernde, session, delete_all_dish_suggestions):
    dataOne = {
        'name': 'Test Dish One',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    
    dataTwo = {
        'name': 'Test Dish Two',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    responseOne = client.post('/create_dish_suggestion',
                json=dataOne,
                headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                )
    
    responseTwo = client.post('/create_dish_suggestion',
                json=dataTwo,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                )
    
    assert responseOne.status_code == 201
    assert responseTwo.status_code == 201
    
    response = client.get('/all_dish_suggestions',
                          headers={'Authorization': f'Bearer {auth_token_hungernde}'})
    
    # Überprüfen der JSON-Antwort
    assert response.status_code == 403
    assert response.json['message'] == f"Zugriff nicht gestattet! all_dish_suggestions Berechtigung erforderlich"

    # Teardown: Entferne die hinzugefügten Datensätze aus der Datenbank
    dish_suggestion_one = session.query(DishSuggestion).filter_by(name=dataOne['name']).first()
    dish_suggestion_two = session.query(DishSuggestion).filter_by(name=dataTwo['name']).first()
    
    if dish_suggestion_one:
        session.delete(dish_suggestion_one)
    if dish_suggestion_two:
        session.delete(dish_suggestion_two)
    session.commit()
    
def test_all_dish_suggestions_no_suggestions(client, auth_token_kantinenmitarbeiter, delete_all_dish_suggestions):
    response = client.get('/all_dish_suggestions',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    # Überprüfen der JSON-Antwort
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"Fehler: Keinen Gerichtsvorschlag gefunden"

def test_dish_suggestion_by_ID_succes_kantinenarbeiter(session, client, auth_token_kantinenmitarbeiter, auth_token_hungernde, delete_all_dish_suggestions):
    
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response_post = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_hungernde}'})

    assert response_post.status_code == 201

    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None

    response_get = client.get(f'/dish_suggestion_by_id/{dish_suggestion.dishSuggestionID}',
                              headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})

    assert response_get.status_code == 200  

    # JSON-Daten des abgerufenen Vorschlags prüfen
    retrieved_dish = response_get.get_json()
    print (retrieved_dish)
    assert retrieved_dish['name'] == new_dish_suggestion['name']
    assert retrieved_dish['description'] == new_dish_suggestion['description']
    assert retrieved_dish['ingredients'] == new_dish_suggestion['ingredients']
    assert retrieved_dish['image'] == new_dish_suggestion['image']
    
def test_dish_suggestion_by_ID_succes_admin(session, client, auth_token_admin, auth_token_hungernde, delete_all_dish_suggestions):
    
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response_post = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_hungernde}'})

    assert response_post.status_code == 201

    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None

    response_get = client.get(f'/dish_suggestion_by_id/{dish_suggestion.dishSuggestionID}',
                              headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_get.status_code == 200  

    # JSON-Daten des abgerufenen Vorschlags prüfen
    retrieved_dish = response_get.get_json()
    print (retrieved_dish)
    assert retrieved_dish['name'] == new_dish_suggestion['name']
    assert retrieved_dish['description'] == new_dish_suggestion['description']
    assert retrieved_dish['ingredients'] == new_dish_suggestion['ingredients']
    assert retrieved_dish['image'] == new_dish_suggestion['image']
    
def test_dish_suggestion_by_ID_no_suggestion(client, auth_token_kantinenmitarbeiter):
    response = client.get(f'/dish_suggestion_by_id/1',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    # Überprüfen der JSON-Antwort
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"Fehler: Gerichtsvorschlag nicht gefunden"