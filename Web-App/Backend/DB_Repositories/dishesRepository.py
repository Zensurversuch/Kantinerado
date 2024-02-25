from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DB_Repositories.models import Dish
import base64
from random import randint

class DishRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def get_dish_by_id(self, dish_id):
        try:
            session = scoped_session(self.session_factory)
            dish_data = session.query(Dish).filter(Dish.dishID == dish_id).first()
            if dish_data:
                allergies = [allergy.name for allergy in dish_data.allergies] if dish_data.allergies else None

                dish_dict = {
                    "dish_id": dish_data.dishID,
                    "name": dish_data.name,
                    "allergies": allergies,
                    "ingredients": dish_data.ingredients,
                    "dietaryCategorie": dish_data.dietaryCategory,
                    "mealType": dish_data.mealType,
                    "image": base64.b64encode(dish_data.image).decode() if dish_data.image else None

                }
                return dish_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def create_dish(self, name, ingredients, dietary_category, meal_type, image=None):
        try:
            session = scoped_session(self.session_factory)
            min_ = 1
            max_ = 1000000000
            rand_dishID = randint(min_, max_)

            while session.query(Dish).filter(Dish.dishID == rand_dishID).first() is not None:
                rand_dishID = randint(min_, max_)

            new_dish = Dish(
                dishID=rand_dishID,
                name=name,
                ingredients=ingredients,
                dietaryCategory=dietary_category,
                mealType=meal_type,
                image=image
            )

            session.add(new_dish)
            session.commit()
            return True
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()
