import base64
import json
import pytest
from unittest.mock import patch
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

def test_create_dish_suggestion_success(client, mock_dish_suggestion_repo, mock_jwt_required, mock_user_repo, mock_get_permissions_for_role):
    # Setze das Mock-Verhalten
    mock_dish_suggestion_repo.create_dishSuggestion.return_value = True
    #mock_user_repo.get_user_by_id.return_value = {'role': 'admin'}

    # Erstelle die Testdaten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
    }

    # Sende die Anfrage
    response = client.post('/create_dish_suggestion',
                           data=json.dumps(data),
                           content_type='application/json'
                           #headers={'Authorization': 'Bearer test_token'}
                           )

    # Überprüfe die Antwort
    print("Response Data:", response.data)
    print("Response JSON:", response.json)
    assert response.status_code == 201
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Gerichtsvorschlag erfolgreich erstellt"

def test_create_dish_suggestion_missing_name(client, mock_dish_suggestion_repo, mock_jwt_required, mock_user_repo, mock_get_permissions_for_role):
    # Setze das Mock-Verhalten
    mock_dish_suggestion_repo.create_dishSuggestion.return_value = False
    mock_user_repo.get_user_by_id.return_value = {'role': 'admin'}
    # Testdaten ohne Namen
    data = {
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
    }

    # Sende die Anfrage
    response = client.post(
        '/create_dish_suggestion',
        data=json.dumps(data),
        content_type='application/json',
        headers={'Authorization': 'Bearer test_token'}
        )

    # Überprüfe die Antwort
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"

def test_create_dish_suggestion_failure(client, mock_dish_suggestion_repo, mock_jwt_required, mock_user_repo, mock_get_permissions_for_role):
    # Setze das Mock-Verhalten
    mock_dish_suggestion_repo.create_dishSuggestion.return_value = False
    #mock_user_repo.get_user_by_id.return_value = {'role': 'admin'}
    # Erstelle die Testdaten
    data = {
        'name': 'Test Dish',
        'ingredients': ['ingredient1', 'ingredient2'],
        'image': base64.b64encode(b'test image data').decode('utf-8')
    }

    # Sende die Anfrage
    response = client.post('/create_dish_suggestion',
                           data=json.dumps(data),
                           content_type='application/json',
                           #headers={'Authorization': 'Bearer test_token'}
                           )

    # Überprüfe die Antwort
    assert response.status_code == 500
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Gerichtsvorschlag konnte nicht erstellt werden"
