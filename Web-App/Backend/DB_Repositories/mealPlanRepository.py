from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from DB_Repositories.models import MealPlan
from datetime import datetime
from random import randint



class MealPlanRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def create_mealPlan(self, mealPlan):
            try:
                session = scoped_session(self.session_factory)
                min_ = 1
                max_ = 1000000000
                rand_mealPlanID = randint(min_, max_)
                for meal in mealPlan:
                    while session.query(MealPlan).filter(MealPlan.mealPlanID == rand_mealPlanID).first() is not None:
                        rand_mealPlanID = randint(min_, max_)
                    dish_id = meal.get('dishID')
                    date_str = meal.get('date')
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    # Speichern der Einträge in der Datenbank
                    new_mealPlan = MealPlan(
                        mealPlanID=rand_mealPlanID,
                        dishID=dish_id,
                        date=date
                    )
                    session.add(new_mealPlan)
                session.commit()
                return True
            except SQLAlchemyError as e:
                return False, e
            except ValueError as e:
                return False, e
            finally:
                session.close()

    def get_mealPlan(self, startDate, endDate):
            try:
                datetime.strptime(startDate, "%Y-%m-%d")
                datetime.strptime(endDate, "%Y-%m-%d")
                session = scoped_session(self.session_factory)
                mealPlan = session.query(MealPlan).filter(MealPlan.date.between(startDate, endDate)).all()
                mealPlan_list = []

                if mealPlan:
                    for meal in mealPlan:
                        meal_dict = {
                            "dishID": meal.dishID,
                            "date": datetime.strftime(meal.date, "%Y-%m-%d")
                        }
                        mealPlan_list.append(meal_dict)

                    return mealPlan_list
                return None
            except ValueError as e:
                return False
            except SQLAlchemyError as e:
                return None
            finally:
                session.close()