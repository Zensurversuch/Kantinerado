from role_permissions import get_permissions_for_role, UserRole, Permissions

def test_available_roles():
    available_roles = ["admin", "hungernde", "kantinenmitarbeiter"]
    assert [role.value for role in UserRole] == available_roles


def test_permissions_for_admin():
    admin_permissions = get_permissions_for_role(UserRole.ADMIN.value)
    expected_permissions = [
        # User Permissions
        Permissions.ALL_USERS.value,
        Permissions.USER_BY_ID.value,
        Permissions.CREATE_USER_AS_ADMIN.value,
        Permissions.SET_USER_ALLERGIES.value,
        # Dish Permissions
        Permissions.DISH_BY_ID.value,
        Permissions.CREATE_DISH.value,
        Permissions.DISH_BY_NAME.value,
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
        Permissions.DISH_SUGGESTION_BY_ID.value,
        Permissions.DELETE_DISH_SUGGESTION.value,
        Permissions.ACCEPT_DISH_SUGGESTION.value
    ]
    assert set(admin_permissions) == set(expected_permissions)

def test_permissions_for_hungernde():
    hungernde_permissions = get_permissions_for_role(UserRole.HUNGERNDE.value)
    expected_permissions = [
        # User Permissions
        Permissions.SET_USER_ALLERGIES.value,
        # Dish Permissions
        Permissions.DISH_BY_ID.value,
        Permissions.DISH_BY_NAME.value,
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
    assert set(hungernde_permissions) == set(expected_permissions)

def test_permissions_for_kantinenmitarbeiter():
    kantinenmitarbeiter_permissions = get_permissions_for_role(UserRole.KANTINENMITARBEITER.value)
    expected_permissions = [
        # Dish Permissions
        Permissions.DISH_BY_ID.value,
        Permissions.CREATE_DISH.value,
        Permissions.DISH_BY_NAME.value,
        Permissions.DISH_BY_MEALTYPE.value,
        # Order Permissions
        Permissions.ORDERS_BY_USER.value,
        Permissions.ORDERS_SORTED_BY_DISH.value,
        # Meal Plan Permissions
        Permissions.MEAL_PLAN.value,
        Permissions.CREATE_MEAL_PLAN.value,
        #Dish suggestion Permissions
        Permissions.ALL_DISH_SUGGESTIONS.value,
        Permissions.DISH_SUGGESTION_BY_ID.value,
        Permissions.DELETE_DISH_SUGGESTION.value,
        Permissions.ACCEPT_DISH_SUGGESTION.value
    ]
    assert set(kantinenmitarbeiter_permissions) == set(expected_permissions)

def test_permissions_for_unknown_role():
    unknown_role_permissions = get_permissions_for_role("unknown_role")
    assert unknown_role_permissions == []