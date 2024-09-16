import pytest
import base64
from DB_Repositories.models import Allergy
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")

########################################################## all_allergies test ##########################################################

def test_all_allergies_success(session, client):
    response = client.get(f'/all_allergies')

    assert response.status_code == 200
    assert response.json == [{'allergieID': 1, 'name': 'TestAllergyOne'}, {'allergieID': 2, 'name': 'TestAllergyTwo'}]
    
def test_all_allergies_no_allergies_available(session, client, delete_all_allergies, reset_allergies):
    response = client.get(f'/all_allergies')

    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Keine Allergien gefunden"