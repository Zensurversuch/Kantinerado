import pytest
from datetime import datetime, timedelta

@pytest.mark.usefixtures("session")

########################################################## week_routes test ##########################################################

def test_get_this_week(client):
    """Test retrieving the Monday and Friday dates of the current week"""

    response = client.get('/get_this_week')
    
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    assert response.status_code == 201
    assert response.json['monday'] == monday.strftime("%Y-%m-%d")
    assert response.json['sunday'] == sunday.strftime("%Y-%m-%d")
    
def test_get_next_week(client):
    """Test retrieving the Monday and Friday dates of the next week"""

    response = client.get('/get_next_week')
    
    today = datetime.today()
    monday = today - timedelta(days=today.weekday()) + timedelta(days=7)
    sunday = monday + timedelta(days=6)

    assert response.status_code == 201
    assert response.json['monday'] == monday.strftime("%Y-%m-%d")
    assert response.json['sunday'] == sunday.strftime("%Y-%m-%d")
    
            
            
