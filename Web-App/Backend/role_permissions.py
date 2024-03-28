def get_permissions_for_role(role):
    for line in permissions_data.split('\n'):
        parts = line.strip().split(':')
        if parts[0] == role:
            return parts[1].split(',')
    return []

permissions_data = """
admin:hello,all_users,user_by_id,user_by_email,dish_by_id,create_dish,allergy_by_userid,create_user_as_admin,dish_by_name,create_dish,create_order,orders_by_user,dish_by_mealType,meal_plan,create_meal_plan,orders_sorted_by_dish,set_user_allergies
hungernde:hello,dish_by_id,allergy_by_userid,dish_by_names,create_order,orders_by_user,dish_by_mealType,meal_plan,set_user_allergies
kantinenmitarbeiter:dish_by_id,create_dish,dish_by_name,create_dish,orders_by_user,dish_by_mealType,meal_plan,create_meal_plan,orders_sorted_by_dish
"""
