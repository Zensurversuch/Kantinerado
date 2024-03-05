from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, Date, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from random import randint
from DB_Repositories.models import Order, MealPlan, Dish



class OrderRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def create_order(self, user_id, meal_plan_id, amount, order_date):
        session = scoped_session(self.session_factory)
        try:
            min_ = 1
            max_ = 1000000000
            rand_orderid = randint(min_, max_)
            while session.query(Order).filter(Order.orderID == rand_orderid).first() is not None:
                rand_orderid = randint(min_, max_)

            new_order = Order(orderID = rand_orderid,
                              userID = user_id,
                              mealPlanID = meal_plan_id,
                              amount = amount,
                              orderDate = order_date)

            session.add(new_order)
            session.commit()
            return True
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()



    def get_orders_by_userid(self, user_id, dateBegin, date_end):
        try:
            session = scoped_session(self.session_factory)

            orders_list = session.query(Order, MealPlan, Dish).join(
                MealPlan, Order.mealPlanID == MealPlan.mealPlanID           # MealPlan = MealPlans which occur in the orders
            ).join(
                Dish, MealPlan.dishID == Dish.dishID        # Dish = Dishes that occur in the MealPlans which occured in the orders
            ).filter(
                and_(
                    Order.userID == user_id,
                    MealPlan.date >= dateBegin,
                    MealPlan.date <= date_end
                )
            ).all()

            final_orders_list = []
            for order, meal_plan, dish in orders_list:
                order_dict = {
                    "orderID": order.orderID,
                    "userID": order.userID,
                    "mealPlanID": order.mealPlanID,
                    "mealPlanDate": meal_plan.date,
                    "mealPlanDishID": dish.dishID,
                    "mealPlanDishName": dish.name,
                    "amount": order.amount,
                    "orderDate": order.orderDate
                }
                final_orders_list.append(order_dict)

            return final_orders_list

        except SQLAlchemyError as e:
            return None

        finally:
            session.close()




    def is_order_already_created(self, userID, meal_plan_id):
        try:
            session = scoped_session(self.session_factory)
            order_data = session.query(Order).filter(Order.userID == userID, Order.mealPlanID == meal_plan_id).first()
            if order_data:
                return True
            return False
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()