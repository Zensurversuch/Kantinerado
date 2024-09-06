import pytest
from flask_jwt_extended import create_access_token
from __init__ import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from initialize_database import initialize_test_database
from DB_Repositories.models import DishSuggestion, Dish, dish_allergy_association

@pytest.fixture(scope='session')
def app():
    """Create and configure the Flask-App for the tests."""
    app = create_app(config_name='testing')
    with app.app_context():
        # Initialize the database schema
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
def delete_all_dish_suggestions(session):
    """Fixture, to delete all dish suggestions from database."""
    session.query(DishSuggestion).delete()
    session.commit()
    
@pytest.fixture(scope='function')
def delete_all_dishes(session):
    """Fixture, to delete all dishes from database."""
    session.query(dish_allergy_association).delete()
    session.query(Dish).delete()
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
