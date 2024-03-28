from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from DB_Repositories.models import Allergy
from random import randint 


class AllergyRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def get_all_allergies(self):
        try:
            session = scoped_session(self.session_factory)
            all_allergies = session.query(Allergy).all()
            allergies_list = []

            if all_allergies:
                for allergy in all_allergies:
                    allergy_dict = {
                        "allergieID": allergy.allergieID,
                        "name": allergy.name
                    }
                    allergies_list.append(allergy_dict)

                return allergies_list
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def get_allergie_by_id(self, param_allergyID):
        try:
            session = scoped_session(self.session_factory)
            allergy_data = session.query(Allergy).filter(Allergy.allergieID == param_allergyID).first()
            if allergy_data:
                allergy_dict = {
                    "allergieID": allergy_data.allergieID,
                    "name": allergy_data.name
                }
                return allergy_dict
            return None
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()
