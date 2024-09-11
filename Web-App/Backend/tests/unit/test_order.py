from datetime import datetime, timedelta
import pytest
from DB_Repositories.models import Dish, MealPlan, Order
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session",)


########################################################## order test ##########################################################

def test_create_order_success_admin(client, auth_token_admin, session, delete_all_orders_mealPlans_dishes):
    """Test creating a order as admin"""
    dish = Dish(
            dishID=1,
            name="Test Dish",
            price= 10.99,
            ingredients=["Test ingredients"],
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        )
    session.add(dish)
    session.commit()

    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date() + timedelta(days=7)
        ),
        MealPlan(
            mealPlanID=2,
            dishID=1, 
            date=datetime.today().date() + timedelta(days=7)
        )
    ]
    session.add_all(mealPlans)
    session.commit(
    )
    # Post-Data
    data = {
          "orders": [
                {
                    "mealPlanID": 1,
                    "amount": 2,
                },
                {
                    "mealPlanID": 2,
                    "amount": 1,
                }
            ]
    }
    response = client.post('/create_order',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Bestellung erfolgreich"
    assert response.status_code == 201

    
    # check if order was created
    first_order = session.query(Order).filter_by(mealPlanID=1).first()
    assert first_order is not None
    assert first_order.amount == 2

    second_order = session.query(Order).filter_by(mealPlanID=2).first()
    assert second_order is not None
    assert second_order.amount == 1
    
def test_create_order_success_hungernde(client, auth_token_hungernde, session, delete_all_orders_mealPlans_dishes):
    """Test creating a order as hungernder"""
    dish = Dish(
            dishID=1,
            name="Test Dish",
            price= 10.99,
            ingredients=["Test ingredients"],
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        )
    session.add(dish)
    session.commit()

    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date() + timedelta(days=7)
        ),
        MealPlan(
            mealPlanID=2,
            dishID=1, 
            date=datetime.today().date() + timedelta(days=7)
        )
    ]
    session.add_all(mealPlans)
    session.commit(
    )
    # Post-Data
    data = {
          "orders": [
                {
                    "mealPlanID": 1,
                    "amount": 2,
                },
                {
                    "mealPlanID": 2,
                    "amount": 1,
                }
            ]
    }
    response = client.post('/create_order',
                           json=data,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )
    
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Bestellung erfolgreich"
    assert response.status_code == 201

    
    # check if order was created
    first_order = session.query(Order).filter_by(mealPlanID=1).first()
    assert first_order is not None
    assert first_order.amount == 2

    second_order = session.query(Order).filter_by(mealPlanID=2).first()
    assert second_order is not None
    assert second_order.amount == 1

def test_orders_by_admin_success(client, auth_token_admin, session, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders by admin within a date range"""
    dish = Dish(
            dishID=1,
            name="Test Dish",
            price= 10.99,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        )
    session.add(dish)
    session.commit()

    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date()
        ),
        MealPlan(
            mealPlanID=2,
            dishID=1, 
            date=datetime.today().date()
        )
    ]
    session.add_all(mealPlans)
    session.commit()

    user_id = 1 

    today = datetime.today().date()
    order1 = Order(userID=user_id, mealPlanID=1, amount=2, orderDate=today - timedelta(days=1))
    order2 = Order(userID=user_id, mealPlanID=2, amount=1, orderDate=today + timedelta(days=1))
    session.add_all([order1, order2])
    session.commit()

    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_by_user/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 200
    response_data = response.json
    assert len(response_data) == 2
    assert any(order['mealPlanID'] == 1 for order in response_data)
    assert any(order['mealPlanID'] == 2 for order in response_data)

def test_orders_by_kantinenmitarbeiter_success(client, auth_token_kantinenmitarbeiter, session, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders by kantinenmitarbeiter within a date range"""
    dish = Dish(
            dishID=1,
            name="Test Dish",
            price= 10.99,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        )
    session.add(dish)
    session.commit()

    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date()
        ),
        MealPlan(
            mealPlanID=2,
            dishID=1, 
            date=datetime.today().date()
        )
    ]
    session.add_all(mealPlans)
    session.commit()

    user_id = 2 

    today = datetime.today().date()
    order1 = Order(userID=user_id, mealPlanID=1, amount=2, orderDate=today - timedelta(days=1))
    order2 = Order(userID=user_id, mealPlanID=2, amount=1, orderDate=today + timedelta(days=1))
    session.add_all([order1, order2])
    session.commit()

    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_by_user/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response.status_code == 200
    response_data = response.json
    assert len(response_data) == 2
    assert any(order['mealPlanID'] == 1 for order in response_data)
    assert any(order['mealPlanID'] == 2 for order in response_data)



def test_orders_by_hungernde_success(client, auth_token_hungernde, session, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders by hungernde within a date range"""
    dish = Dish(
            dishID=1,
            name="Test Dish",
            price= 10.99,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        )
    session.add(dish)
    session.commit()

    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date()
        ),
        MealPlan(
            mealPlanID=2,
            dishID=1, 
            date=datetime.today().date()
        )
    ]
    session.add_all(mealPlans)
    session.commit()

    user_id = 3 

    today = datetime.today().date()
    order1 = Order(userID=user_id, mealPlanID=1, amount=2, orderDate=today - timedelta(days=1))
    order2 = Order(userID=user_id, mealPlanID=2, amount=1, orderDate=today + timedelta(days=1))
    session.add_all([order1, order2])
    session.commit()

    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_by_user/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_hungernde}'})
    
    assert response.status_code == 200
    response_data = response.json
    assert len(response_data) == 2
    assert any(order['mealPlanID'] == 1 for order in response_data)
    assert any(order['mealPlanID'] == 2 for order in response_data)


def test_orders_no_orders_admin(client, auth_token_admin, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders by admin with no orders in the date range"""
    today = datetime.today().date()
    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_by_user/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Sie haben keine Bestellungen in diesem Zeitraum"

def test_orders_no_orders_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders by hungernde with no orders in the date range"""
    today = datetime.today().date()
    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_by_user/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Sie haben keine Bestellungen in diesem Zeitraum"


def test_orders_no_orders_hungernde(client, auth_token_hungernde, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders by hungernde with no orders in the date range"""
    today = datetime.today().date()
    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_by_user/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_hungernde}'})
    
    assert response.status_code == 400
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Sie haben keine Bestellungen in diesem Zeitraum"


def test_orders_sorted_by_dish_success_admin(client, auth_token_admin, session, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders sorted by Dish by admin within a date range"""
    today = datetime.today().date()
    dishes = [
        Dish(
            dishID=1,
            name="Test Dish2",
            price= 10.99,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        ),
        Dish(
            dishID=2,
            name="Test Dish",
            price= 12,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Breakfast",
            image= None,
        )
          ]
    session.add_all(dishes)
    session.commit()
  
    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date()
        ),
        MealPlan(
            mealPlanID=2,
            dishID=2, 
            date=datetime.today().date() + timedelta(days=1)
        )
    ]
    session.add_all(mealPlans)
    session.commit()

    user_id = 1

    order1 = Order(userID=user_id, mealPlanID=1, amount=2, orderDate=today - timedelta(days=1))
    order2 = Order(userID=user_id, mealPlanID=1, amount=1, orderDate=today + timedelta(days=1))
    order3 = Order(userID=user_id, mealPlanID=2, amount=4, orderDate=today)
    session.add_all([order1, order2, order3])
    session.commit()

    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_sorted_by_dish/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 200
    response_data = response.json
    assert len(response_data) == 2
    assert any(
        any(dish['dishID'] == 1 and dish['amount'] == 3 for dish in order['dishes'])
        for order in response_data
    )
    assert any(
        any(dish['dishID'] == 2 and dish['amount'] == 4 for dish in order['dishes'])
        for order in response_data
    )

    
def test_sorted_by_dish_no_orders_admin(client, auth_token_admin, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders sorted by Dish by admin ID with no orders in the date range"""
    today = datetime.today().date()
    start_date = today - timedelta(days=10)
    end_date = today - timedelta(days=5)

    response = client.get(f'/orders_sorted_by_dish/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_admin}'})
    
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Es gibt keine Bestellungen in diesem Zeitraum"

def test_orders_sorted_by_dish_success_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, session, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders sorted by Dish by kantinenmitarbeiter within a date range"""
    today = datetime.today().date()

    dishes = [
        Dish(
            dishID=1,
            name="Test Dish2",
            price= 10.99,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Lunch",
            image= None,
        ),
        Dish(
            dishID=2,
            name="Test Dish",
            price= 12,
            ingredients= None,
            dietaryCategory="Test category",
            mealType="Breakfast",
            image= None,
        )
          ]
    session.add_all(dishes)
    session.commit()
  
    mealPlans = [
        MealPlan(
            mealPlanID=1,
            dishID=1,  
            date=datetime.today().date()
        ),
        MealPlan(
            mealPlanID=2,
            dishID=2, 
            date=datetime.today().date() + timedelta(days=1)
        )
    ]
    session.add_all(mealPlans)
    session.commit()

    user_id = 1

    order1 = Order(userID=user_id, mealPlanID=1, amount=2, orderDate=today - timedelta(days=1))
    order2 = Order(userID=user_id, mealPlanID=1, amount=1, orderDate=today + timedelta(days=1))
    order3 = Order(userID=user_id, mealPlanID=2, amount=4, orderDate=today)
    session.add_all([order1, order2, order3])
    session.commit()

    start_date = today - timedelta(days=5)
    end_date = today + timedelta(days=5)

    response = client.get(f'/orders_sorted_by_dish/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response.status_code == 200
    response_data = response.json
    assert len(response_data) == 2
    assert any(
        any(dish['dishID'] == 1 and dish['amount'] == 3 for dish in order['dishes'])
        for order in response_data
    )
    assert any(
        any(dish['dishID'] == 2 and dish['amount'] == 4 for dish in order['dishes'])
        for order in response_data
    )

def test_sorted_by_dish_no_orders_kantinenmitarbeiter(client, auth_token_kantinenmitarbeiter, delete_all_orders_mealPlans_dishes):
    """Test retrieving orders sorted by Dish by kantinenmitarbeiter with no orders in the date range"""
    today = datetime.today().date()
    start_date = today - timedelta(days=10)
    end_date = today - timedelta(days=5)

    response = client.get(f'/orders_sorted_by_dish/{start_date}/{end_date}',
                          headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})
    
    assert response.status_code == 404
    assert response.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Es gibt keine Bestellungen in diesem Zeitraum"