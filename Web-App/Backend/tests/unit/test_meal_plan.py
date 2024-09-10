import pytest
import base64
from DB_Repositories.models import MealPlan, Dish
from api_messages import get_api_messages, API_MESSAGE_DESCRIPTOR

@pytest.mark.usefixtures("session")

########################################################## create_meal_plan test ##########################################################

def test_create_meal_plan_success_admin(app, client, auth_token_admin, session, delete_all_dishes, delete_all_meal_plans):
    """Test creating a meal plan as admin."""
    newDishOne = {
        'name': 'Test Dish one',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    newDishTwo = {
        'name': 'Test Dish two',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    responsedishOne = client.post('/create_dish',
                           json=newDishOne,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    responsedishTwo = client.post('/create_dish',
                           json=newDishTwo,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responsedishOne.status_code == 201
    assert responsedishTwo.status_code == 201
    
    # check if dish suggestion was created
    dishOne = session.query(Dish).filter_by(name='Test Dish one').first()
    dishTwo = session.query(Dish).filter_by(name='Test Dish two').first()

    mealPlanData = {
        "mealPlan" :
        [
            {
                "dishID": dishOne.dishID,
                "date": "2024-04-03"
            },
            {
                "dishID": dishTwo.dishID,
                "date": "2024-04-04"
            }
        ]
    }
    
    responseMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responseMealPlan.status_code == 201
    assert responseMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Speiseplan erfolgreich erstellt"
    
    mealPlanOne = session.query(MealPlan).filter_by(dishID=dishOne.dishID).first()
    mealPlanTwo = session.query(MealPlan).filter_by(dishID=dishTwo.dishID).first()
    
    assert mealPlanOne is not None
    assert mealPlanTwo is not None
    
def test_create_meal_plan_success_kantinenarbeiter(app, client, auth_token_kantinenmitarbeiter, session, delete_all_dishes, delete_all_meal_plans):
    """Test creating a meal plan as kantinenarbeiter."""
    newDishOne = {
        'name': 'Test Dish one',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    newDishTwo = {
        'name': 'Test Dish two',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    responsedishOne = client.post('/create_dish',
                           json=newDishOne,
                           headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'}
                           )
    responsedishTwo = client.post('/create_dish',
                           json=newDishTwo,
                           headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'}
                           )
    
    assert responsedishOne.status_code == 201
    assert responsedishTwo.status_code == 201
    
    # check if dish suggestion was created
    dishOne = session.query(Dish).filter_by(name='Test Dish one').first()
    dishTwo = session.query(Dish).filter_by(name='Test Dish two').first()

    mealPlanData = {
        "mealPlan" :
        [
            {
                "dishID": dishOne.dishID,
                "date": "2024-04-03"
            },
            {
                "dishID": dishTwo.dishID,
                "date": "2024-04-04"
            }
        ]
    }
    
    responseMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'}
                           )
    
    assert responseMealPlan.status_code == 201
    assert responseMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Speiseplan erfolgreich erstellt"
    
    mealPlanOne = session.query(MealPlan).filter_by(dishID=dishOne.dishID).first()
    mealPlanTwo = session.query(MealPlan).filter_by(dishID=dishTwo.dishID).first()
    
    assert mealPlanOne is not None
    assert mealPlanTwo is not None
    
def test_create_meal_plan_ungernder(app, client, auth_token_admin, auth_token_hungernde, session, delete_all_dishes, delete_all_meal_plans):
    """Test creating a meal plan as hungernder."""
    newDishOne = {
        'name': 'Test Dish one',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    newDishTwo = {
        'name': 'Test Dish two',
        'price': 17.23,
        'ingredients': ['ingredient1', 'ingredient2'],
        'dietaryCategory': 'Test category',
        'mealType': 'Test type',
        'image': base64.b64encode(b'test image data').decode('utf-8'),
        'allergies': ['TestAllergyOne', 'TestAllergyTwo']
    }
    responsedishOne = client.post('/create_dish',
                           json=newDishOne,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    responsedishTwo = client.post('/create_dish',
                           json=newDishTwo,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responsedishOne.status_code == 201
    assert responsedishTwo.status_code == 201
    
    # check if dish suggestion was created
    dishOne = session.query(Dish).filter_by(name='Test Dish one').first()
    dishTwo = session.query(Dish).filter_by(name='Test Dish two').first()

    mealPlanData = {
        "mealPlan" :
        [
            {
                "dishID": dishOne.dishID,
                "date": "2024-04-03"
            },
            {
                "dishID": dishTwo.dishID,
                "date": "2024-04-04"
            }
        ]
    }
    
    responseMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_hungernde}'}
                           )
    
    assert responseMealPlan.status_code == 403
    assert responseMealPlan.json[f"API_MESSAGE_DESCRIPTOR"] == f"Zugriff nicht gestattet! create_meal_plan Berechtigung erforderlich"