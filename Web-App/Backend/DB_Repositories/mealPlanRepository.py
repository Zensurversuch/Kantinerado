from sqlalchemy import Column, Integer, Date, ForeignKey, and_, asc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from DB_Repositories.models import MealPlan, Dish
from datetime import datetime
from random import randint
import base64



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
                
                # Bestimmen des Start- und Enddatums der Woche
                date_str = mealPlan[0].get('date')  # Annahme: Alle Einträge haben das gleiche Datumformat
                date = datetime.strptime(date_str, "%Y-%m-%d")
                week_start = date - timedelta(days=date.weekday())
                week_end = week_start + timedelta(days=6)
                
                # Löschen aller vorhandenen Einträge für die betreffende Woche
                session.query(MealPlan).filter(
                    and_(
                        MealPlan.date >= week_start,
                        MealPlan.date <= week_end
                    )
                ).delete()
                #Hinzufügen aller neuen Eintäge
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
                    return True, str(listOfDuplicates)
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
                mealPlan = session.query(MealPlan, Dish).filter(
                    and_(
                        MealPlan.date >= startDate,
                        MealPlan.date <= endDate,
                        Dish.dishID == MealPlan.dishID
                    )).order_by(asc(MealPlan.date)).all()

                grouped_mealPlans = {}
                if mealPlan:
                    for meal, dish in mealPlan:
                        meal_plan_date = meal.date
                        dish_id = meal.dishID
                        if meal_plan_date not in grouped_mealPlans:
                            grouped_mealPlans[meal_plan_date] = {}
                        if dish_id not in grouped_mealPlans [meal_plan_date]:
                            grouped_mealPlans[meal_plan_date][dish_id] = {
                            "dishID": meal.dishID,
                            "date": datetime.strftime(meal.date, "%Y-%m-%d"),
                            "dishName": dish.name,
                            "dishMealType": dish.mealType,
                            "dishPrice": dish.price,
                            "dishingredients": dish.ingredients,
                            "dishdietaryCategorie": dish.dietaryCategory,
                            "dishmealType": dish.mealType,
                            "dishimage": base64.b64encode(dish.image).decode() if dish.image else None
                        }
                    final_mealPlan_list = []
                    for meal_plan_date, dish_info in grouped_mealPlans.items():
                        dishes = list(dish_info.values())
                        final_mealPlan_list.append({
                            "mealPlanDate": meal_plan_date,
                            "dishes": dishes
                        })

                    return True, final_mealPlan_list
                return None, "mealplan not found"
            except ValueError as e:
                return False, e
            except SQLAlchemyError as e:
                return False, e
            finally:
                session.close()

    def get_mealPlan_dates_by_ids(self, param_mealPlanIDs):
        try:
            session = scoped_session(self.session_factory)
            mealPlans = session.query(MealPlan).filter(MealPlan.mealPlanID.in_(param_mealPlanIDs)).all()
            if mealPlans:
                mealPlanDates = [datetime.strftime(mealplan.date, "%Y-%m-%d") for mealplan in mealPlans]
                return mealPlanDates
            return False
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()
