import pytest
import base64
from DB_Repositories.models import Dish
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")

########################################################## create_dish test ##########################################################

def test_create_dish_success_admin(app, client, auth_token_admin, session, delete_all_dishes):
    new_dish = {
        'name': 'Test Dish',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    
    response = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt"
    
    dish = session.query(Dish).filter_by(name = 'Test Dish').first()
    assert dish is not None
    
def test_create_dish_success_kantinenmitarbeiter(app, client, auth_token_kantinenmitarbeiter, session, delete_all_dishes):
    new_dish = {
        'name': 'Test Dish',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    
    response = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt"
    
    dish = session.query(Dish).filter_by(name = 'Test Dish').first()
    assert dish is not None
    
def test_create_dish_hungernder(client, auth_token_hungernde, session, delete_all_dishes):
    """Test creating a dish suggestion as kantinenmitarbeiter."""
    # Post-Data
    new_dish = {
        'name': 'Test Dish',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    response = client.post('/create_dish',
                            json=new_dish,
                            headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )
    
    assert response.status_code == 403
    assert response.json[f"API_MESSAGE_DESCRIPTOR"] == f"Zugriff nicht gestattet! create_dish Berechtigung erforderlich"
    
    # check if dish suggestion was created
    dish = session.query(Dish).filter_by(name='Test Dish').first()
    assert dish is None
    
    if dish:
            session.delete(dish)
            session.commit()
            
def test_create_dish_already_created(app, client, auth_token_admin, session, delete_all_dishes):
    new_dish = {
        'name': 'Test Dish',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    
    response = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gericht erfolgreich erstellt"
    
    dish = session.query(Dish).filter_by(name = 'Test Dish').first()
    assert dish is not None
    
    response = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Gericht existiert bereits"
    
def test_create_dish_missing_fields(app, client, auth_token_admin, session, delete_all_dishes):
    new_dish = {
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    
    response = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"
    
    dish = session.query(Dish).filter_by(name = 'Test Dish').first()
    assert dish is None
    
def test_create_dish_missing_allergies(app, client, auth_token_admin, session, delete_all_dishes):
    new_dish = {
        'name': 'Test Dish',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo', 'TestAllergyThree']
    }
    
    response = client.post('/create_dish',
                                json=new_dish,
                                headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.WARNING.value}Gericht erfolgreich erstellt, aber die folgenden Allerigie ['TestAllergyThree'] sind nicht in der Datenbank vorhanden"
    
    dish = session.query(Dish).filter_by(name = 'Test Dish').first()
    assert dish is not None