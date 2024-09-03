import pytest
from role_permissions import get_permissions_for_role, UserRole, Permissions

def test_permissions_for_admin():
    admin_permissions = get_permissions_for_role(UserRole.ADMIN.value)
    expected_permissions = [
        Permissions.ALL_USERS.value,
        Permissions.USER_BY_ID.value,
        Permissions.USER_BY_EMAIL.value,
        Permissions.CREATE_USER_AS_ADMIN.value,
        Permissions.SET_USER_ALLERGIES.value,
        Permissions.DISH_BY_ID.value,
        Permissions.CREATE_DISH.value,
        Permissions.DISH_BY_NAME.value,
        Permissions.DISH_BY_MEALTYPE.value,
        Permissions.ALLERGY_BY_USERID.value,
        Permissions.CREATE_ORDER.value,
        Permissions.ORDERS_BY_USER.value,
        Permissions.ORDERS_SORTED_BY_DISH.value,
        Permissions.MEAL_PLAN.value,
        Permissions.CREATE_MEAL_PLAN.value,
    ]
    assert set(admin_permissions) == set(expected_permissions)

def test_permissions_for_hungernde():
    hungernde_permissions = get_permissions_for_role(UserRole.HUNGERNDE.value)
    expected_permissions = [
        Permissions.SET_USER_ALLERGIES.value,
        Permissions.DISH_BY_ID.value,
        Permissions.DISH_BY_NAME.value,
        Permissions.DISH_BY_MEALTYPE.value,
        Permissions.ALLERGY_BY_USERID.value,
        Permissions.CREATE_ORDER.value,
        Permissions.ORDERS_BY_USER.value,
        Permissions.MEAL_PLAN.value,
    ]
    assert set(hungernde_permissions) == set(expected_permissions)

def test_permissions_for_kantinenmitarbeiter():
    kantinenmitarbeiter_permissions = get_permissions_for_role(UserRole.KANTINENMITARBEITER.value)
    expected_permissions = [
        Permissions.DISH_BY_ID.value,
        Permissions.CREATE_DISH.value,
        Permissions.DISH_BY_NAME.value,
        Permissions.DISH_BY_MEALTYPE.value,
        Permissions.ORDERS_BY_USER.value,
        Permissions.ORDERS_SORTED_BY_DISH.value,
        Permissions.MEAL_PLAN.value,
        Permissions.CREATE_MEAL_PLAN.value,
    ]
    assert set(kantinenmitarbeiter_permissions) == set(expected_permissions)
