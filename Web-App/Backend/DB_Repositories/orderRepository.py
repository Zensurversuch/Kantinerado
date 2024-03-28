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

    def create_order(self, param_userID, param_Orders):
        session = scoped_session(self.session_factory)
        
        try:
            for order in param_Orders:
                mealPlanID = order.get('mealPlanID')
                amount = order.get('amount')
                min_ = 1
                max_ = 1000000000
                rand_orderid = randint(min_, max_)
                while session.query(Order).filter(Order.orderID == rand_orderid).first() is not None:
                    rand_orderid = randint(min_, max_)

                today_date = datetime.today().strftime('%Y-%m-%d')

                order_data = self.is_order_already_created(param_userID, mealPlanID)
                if order_data is not False:
                    order_data.amount = amount
                    session.add(order_data)
                    session.commit()
                else:
                    new_order = Order(orderID = rand_orderid,
                                    userID = param_userID,
                                    mealPlanID = mealPlanID,
                                    amount = amount,
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
                if order.amount > 0:
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

    def get_orders_sorted_by_dish(self, param_dateBegin, param_dateEnd):
        try:
            session = scoped_session(self.session_factory)

            orders_list = session.query(Order, MealPlan, Dish).filter(
                and_(
                    MealPlan.date >= param_dateBegin,
                    MealPlan.date <= param_dateEnd,
                    Order.mealPlanID == MealPlan.mealPlanID,
                    Dish.dishID == MealPlan.dishID
                )
            ).order_by(asc(MealPlan.date)).all()

            grouped_orders = {}
            for order, meal_plan, dish in orders_list:
                meal_plan_date = meal_plan.date
                dish_id = dish.dishID
                if order.amount > 0:
                    if meal_plan_date not in grouped_orders:
                        grouped_orders[meal_plan_date] = {}
                    if dish_id not in grouped_orders[meal_plan_date]:
                        grouped_orders[meal_plan_date][dish_id] = {
                            "dishID": dish.dishID,
                            "dishName": dish.name,
                            "dishMealType": dish.mealType,
                            "mealPlanID": meal_plan.mealPlanID,
                            "dishPrice": dish.price,
                            "amount": 0,
                            "completePrice": 0
                        }
                    grouped_orders[meal_plan_date][dish_id]["amount"] += order.amount
                    grouped_orders[meal_plan_date][dish_id]["completePrice"] = int(grouped_orders[meal_plan_date][dish_id]["amount"]) * int(grouped_orders[meal_plan_date][dish_id]["dishPrice"])

            final_orders_list = []
            for meal_plan_date, dish_info in grouped_orders.items():
                dishes = list(dish_info.values())
                final_orders_list.append({
                    "mealPlanDate": meal_plan_date,
                    "dishes": dishes
                })

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