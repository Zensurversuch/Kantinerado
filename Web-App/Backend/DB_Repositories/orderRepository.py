from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from random import randint
from DB_Repositories.models import Order, MealPlan, Dish
from datetime import datetime


class OrderRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)

    def create_order(self, param_userID, param_mealPlanID, param_amount):
        session = scoped_session(self.session_factory)
        try:
            min_ = 1
            max_ = 1000000000
            rand_orderid = randint(min_, max_)
            while session.query(Order).filter(Order.orderID == rand_orderid).first() is not None:
                rand_orderid = randint(min_, max_)

            today_date = datetime.today().strftime('%Y-%m-%d')

            order_data = self.is_order_already_created(param_userID, param_mealPlanID)
            if order_data is not False:
                order_data.amount = order_data.amount + int(param_amount)
                session.add(order_data)
                session.commit()
                return "updated"
            else:
                new_order = Order(orderID = rand_orderid,
                                  userID = param_userID,
                                  mealPlanID = param_mealPlanID,
                                  amount = param_amount,
                                  orderDate = today_date)
                session.add(new_order)
                session.commit()
                return "created"
        except SQLAlchemyError as e:
            return False
        finally:
            session.close()



    def get_orders_by_userid(self, param_userID, param_dateBegin, param_dateEnd):
        try:
            session = scoped_session(self.session_factory)

            orders_list = session.query(Order, MealPlan, Dish).filter (
                and_(
                    MealPlan.date >= param_dateBegin,
                    MealPlan.date <= param_dateEnd,
                    Order.mealPlanID == MealPlan.mealPlanID,
                    Order.userID == param_userID,
                    Dish.dishID == MealPlan.dishID
                )
            ).order_by(asc(MealPlan.date)).all()

            final_orders_list = []
            for order, meal_plan, dish in orders_list:
                order_dict = {
                    "orderID": order.orderID,
                    "userID": order.userID,
                    "mealPlanID": order.mealPlanID,
                    "mealPlanDate": meal_plan.date,
                    "dishID": dish.dishID,
                    "dishName": dish.name,
                    "dishMealType": dish.mealType,
                    "dishPrice": dish.price,
                    "amount": order.amount,
                    "orderPrice": dish.price * order.amount,
                    "orderDate": order.orderDate
                }
                final_orders_list.append(order_dict)

            return final_orders_list
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()



    def is_order_already_created(self, param_userID, param_mealPlanID):
        try:
            session = scoped_session(self.session_factory)
            order_data = session.query(Order).filter(Order.userID == param_userID, Order.mealPlanID == param_mealPlanID).first()
            if order_data:
                return order_data
            return False
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()