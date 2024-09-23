from flask import Flask, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config, TestingConfig, DevelopmentConfig, ProductionConfig
from initialize_database import initialize_Postgres, initialize_test_database
from DB_Repositories import userRepository, dishesRepository, mealPlanRepository, orderRepository, allergyRepository, dishSuggestionRepository
from routes_blueprints import dish_suggestion_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    
    # Konfiguration laden
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'development':
        app.config.from_object(DevelopmentConfig) 
    else:
        app.config.from_object(ProductionConfig)

        
    # Datenbankverbindung initialisieren
    POSTGRES_URL = app.config['POSTGRES_DATABASE_URI']
    engine = create_engine(POSTGRES_URL)
              
    # Repositories bereitstellen
    app.user_repo = userRepository.UserRepository(engine)
    app.dish_repo = dishesRepository.DishRepository(engine)
    app.meal_plan_repo = mealPlanRepository.MealPlanRepository(engine)
    app.order_repo = orderRepository.OrderRepository(engine)
    app.allergy_repo = allergyRepository.AllergyRepository(engine)
    app.dish_suggestion_repo = dishSuggestionRepository.DishSuggestionRepository(engine)
    
    if config_name != 'testing':
        initialize_Postgres(engine)
    # Initialise JWT, CORS and register blueprints
    from flask_jwt_extended import JWTManager
    from flask_cors import CORS
    from routes_blueprints import register_blueprints
    
    jwt = JWTManager(app)
    CORS(app)
    register_blueprints(app)    
    
    if config_name == 'development':
        setup_swagger(app)

    return app

def setup_swagger(app):
    # Swagger UI Konfiguration
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger/swagger.json'  # URL zu deiner swagger.json

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Kantinerado API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    @app.route('/swagger/swagger.json')
    def swagger_json():
        return send_from_directory('swagger', 'swagger.json')  # Richtig den Unterordner angeben
    
    
