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
    
def test_create_meal_plan_hungernder(app, client, auth_token_admin, auth_token_hungernde, session, delete_all_dishes, delete_all_meal_plans):
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
    
def test_create_meal_plan_no_plan_found(app, client, auth_token_admin, session, delete_all_dishes, delete_all_meal_plans):
    """Test creating a meal plan when no meal plan is provided"""

    mealPlanData = {

    }
        
    responseMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responseMealPlan.status_code == 400
    assert responseMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Keine Speisepläne im JSON gefunden"
    
def test_create_meal_plan_missing_fields(app, client, auth_token_admin, session, delete_all_dishes, delete_all_meal_plans):
    """Test creating a meal plan with missing fiels."""

    mealPlanData = {
        "mealPlan" :
        [
            {
                "date": "2024-04-03"
            },
            {
                "dishID": "",
                "date": ""
            }
        ]
    }
    
    responseMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responseMealPlan.status_code == 400
    assert responseMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Fülle alle erforderliche Felder aus"

########################################################## meal_plan test ##########################################################

def test_meal_plan_success_admin(app, client, auth_token_admin, session, delete_all_dishes, delete_all_meal_plans):
    """Test getting a meal plan as admin."""
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
                "date": "2024-04-03"
            },
            {
                "dishID": dishTwo.dishID,
                "date": "2024-04-04"
            },
            {
                "dishID": dishOne.dishID,
                "date": "2024-04-02"
            },
            {
                "dishID": dishOne.dishID,
                "date": "2024-04-05"
            }
        ]
    }
    
    responseCreateMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responseCreateMealPlan.status_code == 201
    assert responseCreateMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Speiseplan erfolgreich erstellt"
    
    newMealPlanOne = session.query(MealPlan).filter_by(dishID=dishOne.dishID).first()
    newMealPlanTwo = session.query(MealPlan).filter_by(dishID=dishTwo.dishID).first()
    
    assert newMealPlanOne is not None
    assert newMealPlanTwo is not None
    
    response_get = client.get(f'/meal_plan/2024-04-03/2024-04-04',
                              headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_get.status_code == 201
    
    mealPlan = response_get.get_json()
    
    assert mealPlan[0]['dishes'][0]['dishID'] == dishOne.dishID
    assert mealPlan[0]['dishes'][0]['date'] == "2024-04-03"
    
    assert mealPlan[0]['dishes'][1]['dishID'] == dishTwo.dishID
    assert mealPlan[0]['dishes'][1]['date'] == "2024-04-03"
    
    assert mealPlan[1]['dishes'][0]['dishID'] == dishTwo.dishID
    assert mealPlan[1]['dishes'][0]['date'] == "2024-04-04"
    
def test_meal_plan_success_hungernder(app, client, auth_token_hungernde, auth_token_admin, session, delete_all_dishes, delete_all_meal_plans):
    """Test getting a meal plan as hungernder."""
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
                "date": "2024-04-03"
            },
            {
                "dishID": dishTwo.dishID,
                "date": "2024-04-04"
            }
        ]
    }
    
    responseCreateMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_admin}'}
                           )
    
    assert responseCreateMealPlan.status_code == 201
    assert responseCreateMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Speiseplan erfolgreich erstellt"
    
    newMealPlanOne = session.query(MealPlan).filter_by(dishID=dishOne.dishID).first()
    newMealPlanTwo = session.query(MealPlan).filter_by(dishID=dishTwo.dishID).first()
    
    assert newMealPlanOne is not None
    assert newMealPlanTwo is not None
    
    response_get = client.get(f'/meal_plan/2024-04-03/2024-04-04',
                              headers={'Authorization': f'Bearer {auth_token_hungernde}'})

    assert response_get.status_code == 201
    
    mealPlan = response_get.get_json()
    
    assert mealPlan[0]['dishes'][0]['dishID'] == dishOne.dishID
    assert mealPlan[0]['dishes'][0]['date'] == "2024-04-03"
    
    assert mealPlan[0]['dishes'][1]['dishID'] == dishTwo.dishID
    assert mealPlan[0]['dishes'][1]['date'] == "2024-04-03"
    
    assert mealPlan[1]['dishes'][0]['dishID'] == dishTwo.dishID
    assert mealPlan[1]['dishes'][0]['date'] == "2024-04-04"
    
def test_meal_plan_success_kantinenarbeiter(app, client, auth_token_kantinenmitarbeiter,session, delete_all_dishes, delete_all_meal_plans):
    """Test getting a meal plan as kantinenarbeiter."""
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
                "date": "2024-04-03"
            },
            {
                "dishID": dishTwo.dishID,
                "date": "2024-04-04"
            }
        ]
    }
    
    responseCreateMealPlan = client.post('/create_meal_plan',
                           json=mealPlanData,
                           headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'}
                           )
    
    assert responseCreateMealPlan.status_code == 201
    assert responseCreateMealPlan.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.SUCCESS.value}Speiseplan erfolgreich erstellt"
    
    newMealPlanOne = session.query(MealPlan).filter_by(dishID=dishOne.dishID).first()
    newMealPlanTwo = session.query(MealPlan).filter_by(dishID=dishTwo.dishID).first()
    
    assert newMealPlanOne is not None
    assert newMealPlanTwo is not None
    
    response_get = client.get(f'/meal_plan/2024-04-03/2024-04-04',
                              headers={'Authorization': f'Bearer {auth_token_kantinenmitarbeiter}'})

    assert response_get.status_code == 201
    
    mealPlan = response_get.get_json()
    
    assert mealPlan[0]['dishes'][0]['dishID'] == dishOne.dishID
    assert mealPlan[0]['dishes'][0]['date'] == "2024-04-03"
    
    assert mealPlan[0]['dishes'][1]['dishID'] == dishTwo.dishID
    assert mealPlan[0]['dishes'][1]['date'] == "2024-04-03"
    
    assert mealPlan[1]['dishes'][0]['dishID'] == dishTwo.dishID
    assert mealPlan[1]['dishes'][0]['date'] == "2024-04-04"
    
def test_meal_plan_not_found(app, client, auth_token_admin, session, delete_all_dishes, delete_all_meal_plans):
    """Test getting a meal plan with no meal plan withing dates."""
    
    response_get = client.get(f'/meal_plan/2024-04-03/2024-04-04',
                              headers={'Authorization': f'Bearer {auth_token_admin}'})

    assert response_get.status_code == 404
    assert response_get.json[API_MESSAGE_DESCRIPTOR] == f"{get_api_messages.ERROR.value}Kein Speiseplan im gewählten Zeitraum gefunden"

    
    