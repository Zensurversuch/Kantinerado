from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DB_Repositories.models import DishSuggestion
import base64
from datetime import date
from random import randint

class DishSuggestionRepository:
    def create_dishSuggestion(self, param_name, param_ingredients=None, param_image=None):
        try:
            session = scoped_session(self.session_factory)
            min_ = 1
            max_ = 1000000000
            rand_dishSuggestionID = randint(min_, max_)

            while session.query(DishSuggestion).filter(DishSuggestion.dishSuggestionId == rand_dishSuggestionID).first() is not None:
                rand_dishSuggestionID = randint(min_, max_)

            new_dishSuggestion = DishSuggestion(
                dishSuggestionID=rand_dishSuggestionID,
                name=param_name,
                ingredients=param_ingredients,
                image=param_image,
                accepted = False,
                date = date.today()
            )

            session.add(new_dishSuggestion)
            session.commit()
            return True
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()