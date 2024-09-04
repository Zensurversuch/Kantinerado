import os

class Config:
    """basic configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@database/{os.getenv('POSTGRES_DB')}"
class DevelopmentConfig(Config):
    """development configuration."""
    DEBUG = True
class TestingConfig(Config):
    """test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:test@localhost:5433/postgres_test"

class ProductionConfig(Config):
    """production configuration"""
