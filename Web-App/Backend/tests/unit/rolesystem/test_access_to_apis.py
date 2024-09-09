import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import patch
from role_permissions import UserRole, get_permissions_for_role
from api_messages import API_MESSAGE_DESCRIPTOR
from DB_Repositories.models import Dish, User, Allergy


############################# Test single get route (/all_users) #########################################
def test_admin_can_access_all_users(client, auth_token_admin, app):
    """Test if an admin can access the all_users route."""
    response = client.get('/all_users',
                          headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response.status_code != 403



def test_kantinenmitarbeiter_cannot_access_all_users(client, auth_token_kantinenmitarbeiter, app):
    """Test if kantinenmitarbeiter can not access the all_users route."""
    response = client.get('/all_users',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})

    assert response.status_code == 403

    message = response.json.get(f"API_MESSAGE_DESCRIPTOR")
    assert message.startswith("Zugriff nicht gestattet!")


def test_hungernde_cannot_access_all_users(client, auth_token_hungernde, app):
    """Test if hungernder can not access the all_users route."""

    response = client.get('/all_users',
                          headers={'Authorization': f'Bearer {auth_token_hungernde}'})

    assert response.status_code == 403

    message = response.json.get(f"API_MESSAGE_DESCRIPTOR")
    assert message.startswith("Zugriff nicht gestattet!")


############################# Test single post route (/create_dish) #########################################
def test_admin_can_access_create_dish(client, auth_token_admin, app, session, delete_all_dishes):
    """Test if an admin can access the create_dish route."""

    response = client.post('/create_dish',
                           headers={'Authorization': f'Bearer {auth_token_admin}'},
                           json={"name": "TestNewCreatedDish", "mealType": "Breakfast", "price": 1.0, "ingredients": "TestIngredients", "dietaryCategory": "TestDietaryCategory"}
                          )
    assert response.status_code == 201

    dish = session.query(Dish).filter_by(name='TestNewCreatedDish').first()
    assert dish is not None
    assert dish.name == 'TestNewCreatedDish'

    if dish:
            session.delete(dish)
            session.commit()


def test_kantinenmitarbeiter_cannot_access_create_dish(client, auth_token_kantinenmitarbeiter, app, session, delete_all_dishes):
    """Test if a kantinenmitarbeit can access the create_dish route."""
    response = client.post('/create_dish',
                           headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'},
                           json={"name": "TestNewCreatedDish", "mealType": "Breakfast", "price": 1.0, "ingredients": "TestIngredients", "dietaryCategory": "TestDietaryCategory"}
                           )

    assert response.status_code == 201

    dish = session.query(Dish).filter_by(name='TestNewCreatedDish').first()
    assert dish is not None
    assert dish.name == 'TestNewCreatedDish'

    if dish:
            session.delete(dish)
            session.commit()

def test_hungernde_cannot_access_create_dish(client, auth_token_hungernde, app):
    """Test if a hungernder cannot access the create_dish route."""

    response = client.post('/create_dish',
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'},
                           json={"name": "TestNewCreatedDish", "mealType": "Breakfast", "price": 1.0, "ingredients": "TestIngredients", "dietaryCategory": "TestDietaryCategory"}
                           )

    assert response.status_code == 403
    message = response.json.get(f"API_MESSAGE_DESCRIPTOR")
    assert message.startswith("Zugriff nicht gestattet!")
