import os

class Config:
    """Basis-Konfigurationsklasse."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@database/{os.getenv('POSTGRES_DB')}"


class DevelopmentConfig(Config):
    """Entwicklungsumgebungskonfiguration."""
    DEBUG = True

class TestingConfig(Config):
    """Testumgebungskonfiguration."""
    TESTING = True
    JWT_SECRET_KEY = 'your_test_secret_key'  
    JWT_ACCESS_TOKEN_EXPIRES = False  
    SERVER_NAME = 'localhost'  

class ProductionConfig(Config):
    """Produktionsumgebungskonfiguration."""
