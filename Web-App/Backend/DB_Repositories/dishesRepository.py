from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DB_Repositories.models import Dish, Allergy
import base64
from random import randint

class DishRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def get_dish_by_id(self, param_dishID):
        try:
            session = scoped_session(self.session_factory)
            dish_data = session.query(Dish).filter(Dish.dishID == param_dishID).first()
            if dish_data:
                allergies = [allergy.name for allergy in dish_data.allergies] if dish_data.allergies else None

                dish_dict = {
                    "dish_id": dish_data.dishID,
                    "name": dish_data.name,
                    "price": dish_data.price,
                    "allergies": allergies,
                    "ingredients": dish_data.ingredients,
                    "dietaryCategory": dish_data.dietaryCategory,
                    "mealType": dish_data.mealType,
                    "image": base64.b64encode(dish_data.image).decode() if dish_data.image else None

                }
                return dish_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def get_dish_by_name(self, param_name):
        try:
            session = scoped_session(self.session_factory)
            dish_data = session.query(Dish).filter(Dish.name == param_name).first()
            if dish_data:
                allergies = [allergy.name for allergy in dish_data.allergies] if dish_data.allergies else None
                dish_dict = {
                    "dish_id": dish_data.dishID,
                    "name": dish_data.name,
                    "price": dish_data.price,
                    "allergies": allergies,
                    "ingredients": dish_data.ingredients,
                    "dietaryCategory": dish_data.dietaryCategory,
                    "mealType": dish_data.mealType,
                    "image": base64.b64encode(dish_data.image).decode() if dish_data.image else None

                }
                return dish_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close() 

    def get_dishes_by_mealType(self, param_mealType):
        try:
            session = scoped_session(self.session_factory)
            dishes_data = session.query(Dish).filter(Dish.mealType == param_mealType).all()
            dishes_list = []

            if dishes_data:
                for dish in dishes_data:
                    allergies = [allergy.name for allergy in dish.allergies] if dish.allergies else None
                    dish_dict = {
                        "dish_id": dish.dishID,
                        "name": dish.name,
                        "price": dish.price,
                        "allergies": allergies,
                        "ingredients": dish.ingredients,
                        "dietaryCategory": dish.dietaryCategory,
                        "mealType": dish.mealType,
                        "image": base64.b64encode(dish.image).decode() if dish.image else None
                    }
                    dishes_list.append(dish_dict)
                return dishes_list
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()                 

    def create_dish(self, param_name, param_price, param_dietaryCategory, param_mealType, param_ingredients=None, param_image=None, param_allergies=None):
        try:
            session = scoped_session(self.session_factory)
            min_ = 1
            max_ = 1000000000
            rand_dishID = randint(min_, max_)

            while session.query(Dish).filter(Dish.dishID == rand_dishID).first() is not None:
                rand_dishID = randint(min_, max_)

            new_dish = Dish(
                dishID=rand_dishID,
                name=param_name,
                price=param_price,
                ingredients=param_ingredients,
                dietaryCategory=param_dietaryCategory,
                mealType=param_mealType,
                image=param_image
            )

            missing_allergies = []
            if param_allergies:
                for allergy_name in param_allergies:
                    allergy = session.query(Allergy).filter(Allergy.name == allergy_name).first()
                    if allergy:
                        new_dish.allergies.append(allergy)
                    else:
                        missing_allergies.append(allergy_name)

            session.add(new_dish)
            session.commit()
            return missing_allergies
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()
