def get_permissions_for_role(role_permissions, role):
    for line in role_permissions.split('\n'):
        parts = line.strip().split(':')
        if parts[0] == role:
            return parts[1].split(',')
    return []

permissions_data = """
admin:money,users,products,hello
hungernde:products,hello
kantinenmitarbeiter:products,hello
"""
