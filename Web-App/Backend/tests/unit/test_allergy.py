import pytest
import base64
from DB_Repositories.models import Allergy
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")

########################################################## allergy_by_id test ##########################################################

def test_allergy_by_id_success(session, client):
    response = client.get(f'/allergy_by_id/1')

    assert response.status_code == 200  
    allergy = response.get_json()
    assert allergy['allergieID'] == 1
    assert allergy['name'] == 'TestAllergyOne'
    
def test_allergy_by_id_not_found(session, client):
    response = client.get(f'/allergy_by_id/3')

    assert response.status_code == 404  
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Allergie nicht gefunden"
    
########################################################## all_allergies test ##########################################################

def test_all_allergies_success(session, client):
    response = client.get(f'/all_allergies')

    assert response.status_code == 200
    assert response.json == [{'allergieID': 1, 'name': 'TestAllergyOne'}, {'allergieID': 2, 'name': 'TestAllergyTwo'}]
    
def test_all_allergies(session, client, delete_all_allergies, reset_allergies):
    response = client.get(f'/all_allergies')

    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Keine Allergien gefunden"