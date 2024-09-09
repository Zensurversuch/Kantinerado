import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import patch
from role_permissions import UserRole

# @pytest.fixture
# def mock_user_repo():
#     """Fixture to mock the user repository."""
#     with patch('flask.current_app.user_repo') as mock_repo:
#         yield mock_repo


def test_admin_can_access_all_users(client, mock_user_repo, auth_token_admin):
    """Test if an admin can access the all_users route."""
    mock_user_repo.get_user_by_id.return_value = {"id": 1, "role": UserRole.ADMIN.value}
    mock_user_repo.get_all_users.return_value = [{"id": 2, "role": UserRole.HUNGERNDE.value}, {"id": 3, "role": UserRole.KANTINENMITARBEITER.value}]

    response = client.get('/all_users',
                          headers={'Authorization': f'Bearer {auth_token_admin}'} 
                )
    
    assert response.status_code == 200
    assert response.json == [{"id": 2, "role": UserRole.HUNGERNDE.value}, {"id": 3, "role": UserRole.KANTINENMITARBEITER.value}]

    """Test if hungernde and kantinenmitarbeiter can not access the all_users route."""
    


def test_hungernde_cannot_access_create_dish(client, mock_user_repo):
    """Test if a user with 'HUNGERNDE' role cannot access the create_dish route."""
    mock_user_repo.get_user_by_id.return_value = {"id": 2, "role": UserRole.HUNGERNDE.value}

    access_token = create_access_token(identity=2)  # Hungernde
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/create_dish', headers=headers)

    assert response.status_code == 403
    assert "Zugriff nicht gestattet" in response.json['message']


@pytest.mark.usefixtures('mock_user_repo')
def test_kantinenmitarbeiter_can_create_dish(client, mock_user_repo):
    """Test if a user with 'KANTINENMITARBEITER' role can access the create_dish route."""
    mock_user_repo.get_user_by_id.return_value = {"id": 3, "role": UserRole.KANTINENMITARBEITER.value}

    access_token = create_access_token(identity=3)  # Kantinenmitarbeiter
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/create_dish', headers=headers)

    assert response.status_code == 200
    assert response.json == {"msg": "Dish created!"}


@pytest.mark.usefixtures('mock_user_repo')
def test_hungernde_cannot_access_all_users(client, mock_user_repo):
    """Test if a user with 'HUNGERNDE' role cannot access the all_users route."""
    mock_user_repo.get_user_by_id.return_value = {"id": 2, "role": UserRole.HUNGERNDE.value}

    access_token = create_access_token(identity=2)  # Hungernde
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/all_users', headers=headers)

    assert response.status_code == 403
    assert "Zugriff nicht gestattet" in response.json['message']


@pytest.mark.usefixtures('mock_user_repo')
def test_kantinenmitarbeiter_cannot_access_all_users(client, mock_user_repo):
    """Test if a user with 'KANTINENMITARBEITER' role cannot access the all_users route."""
    mock_user_repo.get_user_by_id.return_value = {"id": 3, "role": UserRole.KANTINENMITARBEITER.value}

    access_token = create_access_token(identity=3)  # Kantinenmitarbeiter
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/all_users', headers=headers)

    assert response.status_code == 403
    assert "Zugriff nicht gestattet" in response.json['message']
