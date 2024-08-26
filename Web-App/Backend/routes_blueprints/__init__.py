from flask import Flask
from .user_routes import user_blueprint
from .allergy_routes import allergy_blueprint
from .dish_routes import dish_blueprint
from .order_routes import order_blueprint
from .meal_plan_routes import meal_plan_blueprint
from .week_routes import week_blueprint
from .dishSuggestion_routes import dishSuggestion_blueprint

def register_blueprints(app):
    app.register_blueprint(user_blueprint)
    app.register_blueprint(allergy_blueprint)
    app.register_blueprint(dish_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(meal_plan_blueprint)
    app.register_blueprint(week_blueprint)
    app.register_blueprint(dishSuggestion_blueprint)