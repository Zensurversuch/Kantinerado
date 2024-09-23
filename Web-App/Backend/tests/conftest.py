import json
import os

import pytest
from flask_jwt_extended import create_access_token
from playwright.sync_api import Page, expect

from __init__ import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from initialize_database import initialize_test_database
from DB_Repositories.models import DishSuggestion, Dish, Order, dish_allergy_association, MealPlan, Allergy, User, user_allergy_association

@pytest.fixture(scope='session')
def app():
    """Create and configure the Flask-App for the tests."""
    app = create_app(config_name='unitTesting')
    with app.app_context():
        # Initialize the database schema
        print("Inititalize Database")
        engine = create_engine(app.config['POSTGRES_DATABASE_URI'])
        print(app.config['POSTGRES_DATABASE_URI'])
        initialize_test_database(engine)
        yield app

@pytest.fixture(scope='session')
def client(app):
    """Create and configure a test-client for the App."""
    return app.test_client()

@pytest.fixture(scope='session')
def session(app):
    """Create a SQLAlchemy-Session for tests."""
    engine = create_engine(app.config['POSTGRES_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def delete_all_orders_mealPlans_dishes(session):
    """Fixture, to delete all orders, mealPlans and dishes from database."""
    session.query(Order).delete()
    session.query(MealPlan).delete()
    session.query(dish_allergy_association).delete()
    session.query(Dish).delete()
    session.commit()

@pytest.fixture(scope='function')
def delete_all_dish_suggestions(session):
    """Fixture, to delete all dish suggestions from database."""
    session.query(DishSuggestion).delete()
    session.commit()
    
@pytest.fixture(scope='function')
def delete_all_meal_plans(session):
    """Fixture, to delete all meal plans from database."""
    session.query(MealPlan).delete()
    session.commit()
    
@pytest.fixture(scope='function')
def delete_all_dishes(session):
    """Fixture, to delete all dishes from database."""
    session.query(MealPlan).delete()
    session.query(dish_allergy_association).delete()
    session.query(Dish).delete()
    session.commit()

@pytest.fixture(scope='function')
def delete_all_allergies(session):
    """Fixture, to delete all allergies from database."""
    session.query(dish_allergy_association).delete()
    session.query(user_allergy_association).delete()
    session.query(Allergy).delete()
    session.commit()

@pytest.fixture(scope='function')
def reset_allergies(session, delete_all_allergies):
    """Fixture, to reset allergies in database after a test."""
    yield
    allergies = [
        Allergy(allergieID=1, name='TestAllergyOne'),
        Allergy(allergieID=2, name='TestAllergyTwo'),
        ]
    session.add_all(allergies)
    session.commit()

@pytest.fixture(scope='function')
def delete_all_users(session):
    """Fixture, to delete all users from database except those with userID 1, 2 and 3."""
    session.query(user_allergy_association).delete()
    session.query(User).filter(
        ~User.userID.in_([1, 2, 3])
    ).delete(synchronize_session=False)
    session.commit()
        
@pytest.fixture(scope='function')
def auth_token_admin(app):
    """create an admin jwt-token."""
    with app.app_context():
        return create_access_token(identity=1, expires_delta=False)

@pytest.fixture(scope='function')
def auth_token_kantinenmitarbeiter(app):
    """create a kantinenmitarbeiter jwt-Token."""
    with app.app_context():
        return create_access_token(identity=2, expires_delta=False)
    
@pytest.fixture(scope='function')
def auth_token_hungernde(app):
    """Create an hungernde jwt-Token."""
    with app.app_context():
        return create_access_token(identity=3, expires_delta=False)

@pytest.fixture(scope="function")
def load_users():
    file_path = os.path.join(os.path.dirname(__file__), 'user.json')
    print("loading Usersdata")
    with open(file_path) as f:
        return json.load(f)

def perform_login(page:Page, username, password):
    print("Performing login")
    page.goto("/#/")
    page.get_by_role("button", name="Menu").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="Login").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("/#/login")
    page.get_by_label("Username:").click()
    page.get_by_label("Username:").fill(username)
    page.get_by_label("Password:").click()
    page.get_by_label("Password:").fill(password)
    page.get_by_label("Password:").press("Enter")
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("/#/")

def perform_logout(page:Page):
    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Logout").click()
    page.get_by_role("button", name="Ja, Abmelden").click()
    expect(page).to_have_url("/#/login")
