def get_permissions_for_role(role):
    for line in permissions_data.split('\n'):
        parts = line.strip().split(':')
        if parts[0] == role:
            return parts[1].split(',')
    return []

permissions_data = """
admin:hello,all_users,user_by_id,user_by_email,dish_by_id,create_dish,allergy_by_userid,create_user_as_admin,all_allergies,allergy_by_id
hungernde:hello,dish_by_id,allergy_by_userid,all_allergies,allergy_by_id
kantinenmitarbeiter:dish_by_id,create_dish,all_allergies,allergy_by_id
"""
