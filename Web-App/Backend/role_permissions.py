from enum import Enum

def get_permissions_for_role(role):
    permissions = []
    if role == UserRole.ADMIN.value:
        permissions = [
            # User Permissions
            Permissions.USER_BY_ID.value,   
            Permissions.CREATE_USER_AS_ADMIN.value,
            Permissions.SET_USER_ALLERGIES.value, 
            # Dish Permissions 
            Permissions.CREATE_DISH.value,  
            Permissions.DISH_BY_MEALTYPE.value,  
            # Allergy Permissions
            Permissions.ALLERGY_BY_USERID.value,  
            # Order Permissions
            Permissions.CREATE_ORDER.value,  
            Permissions.ORDERS_BY_USER.value,  
            Permissions.ORDERS_SORTED_BY_DISH.value, 
            # Meal Plan Permissions  
            Permissions.MEAL_PLAN.value,  
            Permissions.CREATE_MEAL_PLAN.value,
            # Dish Suggestion Permissions
            Permissions.CREATE_DISH_SUGGESTION.value,
            Permissions.ALL_DISH_SUGGESTIONS.value,
            Permissions.DELETE_DISH_SUGGESTION.value,
            Permissions.ACCEPT_DISH_SUGGESTION.value
        ]
    elif role == UserRole.HUNGERNDE.value:
        permissions = [
            # User Permissions
            Permissions.SET_USER_ALLERGIES.value, 
            # Dish Permissions
            Permissions.DISH_BY_MEALTYPE.value,  
            # Allergy Permissions
            Permissions.ALLERGY_BY_USERID.value,  
            # Order Permissions
            Permissions.CREATE_ORDER.value, 
            Permissions.ORDERS_BY_USER.value,  
            # Meal Plan Permissions 
            Permissions.MEAL_PLAN.value,
            # Dish Suggestion Permissions
            Permissions.CREATE_DISH_SUGGESTION.value  
        ]
    elif role == UserRole.KANTINENMITARBEITER.value:
        permissions = [
            # Dish Permissions 
            Permissions.CREATE_DISH.value, 
            Permissions.DISH_BY_MEALTYPE.value,               
            # Order Permissions
            Permissions.ORDERS_BY_USER.value,  
            Permissions.ORDERS_SORTED_BY_DISH.value,
            # Meal Plan Permissions
            Permissions.MEAL_PLAN.value,  
            Permissions.CREATE_MEAL_PLAN.value,
            #Dish suggestion Permissions
            Permissions.ALL_DISH_SUGGESTIONS.value,
            Permissions.DELETE_DISH_SUGGESTION.value,
            Permissions.ACCEPT_DISH_SUGGESTION.value
    
        ]
    return permissions

class UserRole(Enum):
    ADMIN = "admin"
    HUNGERNDE = "hungernde"
    KANTINENMITARBEITER = "kantinenmitarbeiter"

    def __str__(self):
        return self.value


class Permissions(Enum):
    # User Permissions
    USER_BY_ID = "user_by_id"
    USER_BY_EMAIL = "user_by_email"
    CREATE_USER_AS_ADMIN = "create_user_as_admin"
    SET_USER_ALLERGIES = "set_user_allergies"
    # Dish Permissions
    CREATE_DISH = "create_dish"
    DISH_BY_MEALTYPE = "dish_by_mealType"
    # Allergy Permissions
    ALLERGY_BY_USERID = "allergy_by_userid"
   
    # Order Permissions
    CREATE_ORDER = "create_order"
    ORDERS_BY_USER = "orders_by_user"
    ORDERS_SORTED_BY_DISH = "orders_sorted_by_dish"
    # Meal Plan Permissions
    MEAL_PLAN = "meal_plan"
    CREATE_MEAL_PLAN = "create_meal_plan"
    
    # Dish Suggestion Permissions
    CREATE_DISH_SUGGESTION = "create_dish_suggestion"
    ALL_DISH_SUGGESTIONS = "all_dish_suggestions"
    DELETE_DISH_SUGGESTION = "delete_dish_suggestion"
    ACCEPT_DISH_SUGGESTION = "accept_dish_suggestion"
    
    def __str__(self):
        return self.value