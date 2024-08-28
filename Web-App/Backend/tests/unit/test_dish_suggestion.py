import pytest
import base64
from DB_Repositories.models import DishSuggestion
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")
def test_create_dish_suggestion_succes_admin(client, auth_token_admin, session):
    """Test creating a dish suggestionas admin."""
    # Post-Daten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
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
def test_create_dish_suggestion_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, session):
    """Test creating a dish suggestion as kantinenmitarbeiter."""
    # Post-Daten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
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
            
            
def test_create_dish_suggestion_succes_hungernde(client, auth_token_hungernde, session):
    """Test creating a dish suggestion as Hungernder"""
    # Post-Daten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
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
            
def test_create_dish_suggestion_missing_name(client, auth_token_hungernde, session):
    # Testdaten ohne Namen
    data = {
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
    }

    response = client.post('/create_dish_suggestion',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )

    # Überprüfe die Antwort
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"

