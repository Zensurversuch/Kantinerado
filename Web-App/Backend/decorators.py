from functools import wraps
from flask_jwt_extended import get_jwt_identity
from role_permissions import get_permissions_for_role
from flask import jsonify

def permission_check(user_repo):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            function_name = func.__name__
            current_user = get_jwt_identity()
            user_data = user_repo.get_user_by_id(current_user)

            if(user_data):
                current_role = user_data["role"]
            else:
                return jsonify({"msg": "Benutzer existiert nicht"}), 401

            current_permissions = set(get_permissions_for_role(current_role))

            if function_name in current_permissions:
                return func(*args, **kwargs)
            else:
                return jsonify(message=f'Zugriff nicht gestattet! {function_name} Berechtigung erforderlich'), 403

        return wrapper
    return decorator
