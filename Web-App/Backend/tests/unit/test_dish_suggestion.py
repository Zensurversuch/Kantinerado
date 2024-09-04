import pytest
import base64
from DB_Repositories.models import DishSuggestion
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")

########################################################## create_dish_suggestions test ##########################################################

def test_create_dish_suggestion_success_admin(client, auth_token_admin, session, delete_all_dish_suggestions):
    """Test creating a dish suggestion as admin."""
    # Post-Data
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
    
    # check if dish suggestion was created
    suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    assert suggestion is not None
    assert suggestion.name == 'Test Dish'
    
    if suggestion:
            session.delete(suggestion)
            session.commit()
            
def test_create_dish_suggestion_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, session, delete_all_dish_suggestions):
    """Test creating a dish suggestion as kantinenmitarbeiter."""
    # Post-Data
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
    
    # check if dish suggestion was created
    suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    assert suggestion is None
    
    if suggestion:
            session.delete(suggestion)
            session.commit()
                      
def test_create_dish_suggestion_success_hungernde(client, auth_token_hungernde, session, delete_all_dish_suggestions):
    """Test creating a dish suggestion as Hungernder"""
    # Post-Data
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
    
    # check if dish suggestion was created
    suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    assert suggestion is not None
    assert suggestion.name == 'Test Dish'
    
    if suggestion:
            session.delete(suggestion)
            session.commit()
            
def test_create_dish_suggestion_missing_name(client, auth_token_hungernde, delete_all_dish_suggestions):
    # Testdata without name
    data = {
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response = client.post('/create_dish_suggestion',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )

    # Validating response
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"
    
########################################################## all_dish_suggestions test ##########################################################

def test_all_dish_suggestions_success_kantinenarbeiter(client, auth_token_kantinenmitarbeiter, auth_token_hungernde, session, delete_all_dish_suggestions):
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
    
    # Validating JSON-response
    response_data = response.get_json()
    print (response_data)
    assert response_data is not None
    assert len(response_data) >= 2 
    
    # check if response includes test data
    dish_names = [dish['name'] for dish in response_data]
    assert dataOne['name'] in dish_names
    assert dataTwo['name'] in dish_names

    dish_suggestion_one = session.query(DishSuggestion).filter_by(name=dataOne['name']).first()
    dish_suggestion_two = session.query(DishSuggestion).filter_by(name=dataTwo['name']).first()
    
    if dish_suggestion_one:
        session.delete(dish_suggestion_one)
    if dish_suggestion_two:
        session.delete(dish_suggestion_two)
    session.commit()
    
def test_all_dish_suggestions_success_admin(client, auth_token_admin, auth_token_hungernde, session, delete_all_dish_suggestions):
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
    
    # Validating JSON-response
    response_data = response.get_json()
    print (response_data)
    assert response_data is not None
    assert len(response_data) >= 2 

    # Validating if response includes test data
    dish_names = [dish['name'] for dish in response_data]
    assert dataOne['name'] in dish_names
    assert dataTwo['name'] in dish_names

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
    
    # Validate the JSON-response
    assert response.status_code == 403
    assert response.json['message'] == f"Zugriff nicht gestattet! all_dish_suggestions Berechtigung erforderlich"

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
    
    # Validating the JSON-response
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"Fehler: Keinen Gerichtsvorschlag gefunden"
       
########################################################## dish_suggestion_by_ID test ##########################################################

def test_dish_suggestion_by_ID_success_kantinenarbeiter(session, client, auth_token_kantinenmitarbeiter, auth_token_hungernde, delete_all_dish_suggestions):
    
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

    # Check JSON-Data of dish suggestion
    retrieved_dish = response_get.get_json()
    print (retrieved_dish)
    assert retrieved_dish['name'] == new_dish_suggestion['name']
    assert retrieved_dish['description'] == new_dish_suggestion['description']
    assert retrieved_dish['ingredients'] == new_dish_suggestion['ingredients']
    assert retrieved_dish['image'] == new_dish_suggestion['image']
    
def test_dish_suggestion_by_ID_success_admin(session, client, auth_token_admin, auth_token_hungernde, delete_all_dish_suggestions):
    
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

    # Check JSON-Data of dish suggestion
    retrieved_dish = response_get.get_json()
    print (retrieved_dish)
    assert retrieved_dish['name'] == new_dish_suggestion['name']
    assert retrieved_dish['description'] == new_dish_suggestion['description']
    assert retrieved_dish['ingredients'] == new_dish_suggestion['ingredients']
    assert retrieved_dish['image'] == new_dish_suggestion['image']
    
def test_dish_suggestion_by_ID_no_suggestion(client, auth_token_kantinenmitarbeiter, delete_all_dish_suggestions):
    response = client.get(f'/dish_suggestion_by_id/1',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    # Validate the JSON-response
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"Fehler: Gerichtsvorschlag nicht gefunden"
    
########################################################## delete_dish_suggestion test ##########################################################
    
def test_delete_dish_suggestion_success_kantinenmitarbeiter(session, client, auth_token_kantinenmitarbeiter, auth_token_hungernde, delete_all_dish_suggestions):
    
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

    response_get = client.get(f'/delete_dish_suggestion/{dish_suggestion.dishSuggestionID}',
                              headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})

    assert response_get.status_code == 201 
    assert response_get.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich gelöscht"

def test_delete_dish_suggestion_success_admin(session, client, auth_token_admin, auth_token_hungernde, delete_all_dish_suggestions):
    
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

    response_get = client.get(f'/delete_dish_suggestion/{dish_suggestion.dishSuggestionID}',
                              headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_get.status_code == 201 
    assert response_get.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich gelöscht"
    
def test_delete_dish_suggestion_no_suggestion(client, auth_token_kantinenmitarbeiter, delete_all_dish_suggestions):
    response = client.get(f'/dish_suggestion_by_id/1',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"Fehler: Gerichtsvorschlag nicht gefunden"
    
########################################################## accept_dish_suggestion test ##########################################################

def test_accept_dish_suggestion_success_admin(session, client, auth_token_admin, delete_all_dish_suggestions, delete_all_dishes):
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response_postSuggestion = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_postSuggestion.status_code == 201
    
    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None
    
    dishSuggestionID = dish_suggestion.dishSuggestionID
    
    accepted_dish_suggestion = {
        'dishSuggestionID': dishSuggestionID,
        'dishData': {
            'name': 'Test Dish',
            'price': 17.23,
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response_acceptSuggestion.status_code == 201
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt. Gerichtsvorschlag erfolgreich gelöscht"
    
def test_accept_dish_suggestion_success_kantinenmitarbeiter(session, client, auth_token_admin, auth_token_kantinenmitarbeiter, delete_all_dish_suggestions, delete_all_dishes):
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response_postSuggestion = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_postSuggestion.status_code == 201
    
    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None
    
    dishSuggestionID = dish_suggestion.dishSuggestionID
    
    accepted_dish_suggestion = {
        'dishSuggestionID': dishSuggestionID,
        'dishData': {
            'name': 'Test Dish',
            'price': 17.23,
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response_acceptSuggestion.status_code == 201
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt. Gerichtsvorschlag erfolgreich gelöscht"
    
def test_accept_dish_suggestion_missing_fields(session, client, auth_token_admin, delete_all_dish_suggestions, delete_all_dishes):
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response_postSuggestion = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_postSuggestion.status_code == 201
    
    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None
    
    dishSuggestionID = dish_suggestion.dishSuggestionID
    
    accepted_dish_suggestion = {
        'dishData': {
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response_acceptSuggestion.status_code == 400
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderlichen Felder aus"
    
def test_accept_dish_suggestion_dish_already_created(session, client, auth_token_admin, delete_all_dish_suggestions, delete_all_dishes):
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }
    
    new_dish = {
        'name': 'Test Dish',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }

    response_postSuggestion = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    response_postDish = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_postSuggestion.status_code == 201
    assert response_postDish.status_code == 201
    
    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None
    
    dishSuggestionID = dish_suggestion.dishSuggestionID
    
    accepted_dish_suggestion = {
        'dishSuggestionID': dishSuggestionID,
        'dishData': {
            'name': 'Test Dish',
            'price': 17.23,
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response_acceptSuggestion.status_code == 400
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Gericht existiert bereits"
    
def test_accept_dish_suggestion_suggestion_not_deleted(session, client, auth_token_admin, delete_all_dish_suggestions, delete_all_dishes):
    
    accepted_dish_suggestion = {
        'dishSuggestionID': 1,
        'dishData': {
            'name': 'Test Dish',
            'price': 17.23,
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response_acceptSuggestion.status_code == 201
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt. Gerichtsvorschlag konnte nicht gelöscht werden"
    
def test_accept_dish_suggestion_missing_allergies(session, client, auth_token_admin, delete_all_dish_suggestions, delete_all_dishes):
    new_dish_suggestion = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'description': 'Das ist eine Testbeschreibung'
    }

    response_postSuggestion = client.post('/create_dish_suggestion',
                                json=new_dish_suggestion,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_postSuggestion.status_code == 201
    
    dish_suggestion = session.query(DishSuggestion).filter_by(name='Test Dish').first()
    
    assert dish_suggestion is not None
    
    dishSuggestionID = dish_suggestion.dishSuggestionID
    
    accepted_dish_suggestion = {
        'dishSuggestionID': dishSuggestionID,
        'dishData': {
            'name': 'Test Dish',
            'price': 17.23,
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response_acceptSuggestion.status_code == 201
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allerigie ['TestAllergyThree'] sind nicht in der Datenbank vorhanden Gerichtsvorschlag erfolgreich gelöscht"
    
def test_accept_dish_suggestion_missing_allergies_not_deleted(session, client, auth_token_admin, delete_all_dish_suggestions, delete_all_dishes):
    
    accepted_dish_suggestion = {
        'dishSuggestionID': 1,
        'dishData': {
            'name': 'Test Dish',
            'price': 17.23,
            'ingredients': ['ingredient1', 'ingredient2'],
            'dietaryCategory': 'Test category',
            'mealType': 'Test type',
            'image': base64.b64encode(b'test image data').decode('utf-8'),
            'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
        }
    }
    
    response_acceptSuggestion = client.post('/accept_dish_suggestion',
                json = accepted_dish_suggestion,
                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response_acceptSuggestion.status_code == 201
    assert response_acceptSuggestion.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allerigie ['TestAllergyThree'] sind nicht in der Datenbank vorhanden Gerichtsvorschlag konnte nicht gelöscht werden"