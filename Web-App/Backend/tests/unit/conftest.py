import pytest
from flask_jwt_extended import create_access_token
from __init__ import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from initialize_database import initialize_test_database
from DB_Repositories.models import DishSuggestion, Dish, dish_allergy_association

@pytest.fixture(scope='session')
def app():
    """Erstelle und konfiguriere die Flask-Anwendung für die Tests."""
    app = create_app(config_name='testing')
    with app.app_context():
        # Initialize the database schema
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        initialize_test_database(engine)
    yield app

@pytest.fixture(scope='session')
def client(app):
    """Erstelle und konfiguriere einen Test-Client für die Anwendung."""
    return app.test_client()

@pytest.fixture(scope='session')
def session(app):
    """Erstelle eine SQLAlchemy-Session für Tests."""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def delete_all_dish_suggestions(session):
    """Fixture, um alle Gerichtsvorschläge in der Datenbank vor jedem Test zu löschen."""
    session.query(DishSuggestion).delete()
    session.commit()
    
@pytest.fixture(scope='function')
def delete_all_dishes(session):
    """Fixture, um alle Gerichte in der Datenbank vor jedem Test zu löschen."""
    session.query(dish_allergy_association).delete()
    session.query(Dish).delete()
    session.commit()
        
@pytest.fixture(scope='function')
def auth_token_admin(app):
    """Erstelle einen admin JWT-Token für Tests."""
    with app.app_context():
        return create_access_token(identity=1, expires_delta=False)

@pytest.fixture(scope='function')
def auth_token_kantinenmitarbeiter(app):
    """Erstelle einen kantinenmitarbeiter JWT-Token für Tests."""
    with app.app_context():
        return create_access_token(identity=2, expires_delta=False)
    
@pytest.fixture(scope='function')
def auth_token_hungernde(app):
    """Erstelle einen hungernde JWT-Token für Tests."""
    with app.app_context():
        return create_access_token(identity=3, expires_delta=False)
