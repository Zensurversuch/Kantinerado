from sqlalchemy import create_engine
from DB_Repositories import userRepository, dishesRepository, orderRepository, mealPlanRepository, allergyRepository, dishSuggestionRepository
from initialize_database import initialize_Postgres
import os

POSTGRES_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@database/{os.getenv('POSTGRES_DB')}"

engine = create_engine(POSTGRES_URL)

# Repositories
user_repo = userRepository.UserRepository(engine)
dish_repo = dishesRepository.DishRepository(engine)
meal_plan_repo = mealPlanRepository.MealPlanRepository(engine)
order_repo = orderRepository.OrderRepository(engine)
allergy_repo = allergyRepository.AllergyRepository(engine)
dish_suggestion_repo = dishSuggestionRepository.DishSuggestionRepository(engine)

# Postgres Database
initialize_Postgres(engine)