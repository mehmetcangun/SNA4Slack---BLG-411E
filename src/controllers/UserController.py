from ..models.Users import UserQuery
from flask import session

def save_user(ip_address, device_type):
    try:
        current_client_id = UserQuery(ip_address=ip_address, device_type=device_type).insert()
        session["current_client_id"] = current_client_id
    except Exception as e:
        print(e)

def get_user_count():
    return UserQuery.find_user_count()

def get_user_count_having_files():
    return UserQuery.find_user_count_having_files()
    
