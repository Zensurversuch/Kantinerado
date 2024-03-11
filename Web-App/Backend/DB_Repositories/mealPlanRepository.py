from sqlalchemy import Column, Integer, Date, ForeignKey, and_
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
                listOfDuplicates = []
                rand_mealPlanID = randint(min_, max_)
                for meal in mealPlan:
                    dish_id = meal.get('dishID')
                    date_str = meal.get('date')
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    if not session.query(MealPlan).filter(
                        and_(
                            MealPlan.date == date,
                            MealPlan.dishID == dish_id
                        )
                    ).first():
                        while session.query(MealPlan).filter(MealPlan.mealPlanID == rand_mealPlanID).first() is not None:
                            rand_mealPlanID = randint(min_, max_)
                        # Speichern der Einträge in der Datenbank
                        new_mealPlan = MealPlan(
                            mealPlanID=rand_mealPlanID,
                            dishID=dish_id,
                            date=date
                        )
                        session.add(new_mealPlan)
                    else:
                        listOfDuplicates.append(meal)
                session.commit()
                if listOfDuplicates == []:
                    return True, ''
                else: 
                    return True, str(listOfDuplicates)+" were already added"
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

                    return True, mealPlan_list
                return False, "mealplan not found"
            except ValueError as e:
                return False, e
            except SQLAlchemyError as e:
                return False, e
            finally:
                session.close()