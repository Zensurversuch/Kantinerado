from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DB_Repositories.models import DishSuggestion
import base64
from datetime import date
from random import randint

class DishSuggestionRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)
        
    def create_dishSuggestion(self, param_name, param_ingredients=None, param_image=None, param_description=None):
        try:
            session = scoped_session(self.session_factory)
            min_ = 1
            max_ = 1000000000
            rand_dishSuggestionID = randint(min_, max_)

            while session.query(DishSuggestion).filter(DishSuggestion.dishSuggestionID == rand_dishSuggestionID).first() is not None:
                rand_dishSuggestionID = randint(min_, max_)

            new_dishSuggestion = DishSuggestion(
                dishSuggestionID=rand_dishSuggestionID,
                name=param_name,
                ingredients=param_ingredients,
                image=param_image,
                description=param_description,
                date = date.today()
            )
            session.add(new_dishSuggestion)
            session.commit()
            return True
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()
            
    def get_all_users(self):
        try:
            session = scoped_session(self.session_factory)
            all_dishSuggestions = session.query(DishSuggestion).all()
            dishSuggestion_list = []

            if all_dishSuggestions:
                for dishSuggestion in all_dishSuggestions:
                    dishSuggestion_dict = {
                        "dishSuggestionID": dishSuggestion.dishSuggestionID,
                        "name": dishSuggestion.name,
                        "date": dishSuggestion.date
                    }
                    dishSuggestion_list.append(dishSuggestion_dict)

                return dishSuggestion_list
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()