# bot/helper.py

import os

def is_user(user_id):
    # Read the user IDs from .env file
    allowed_users = os.getenv('USER_ID').split(',')
    if str(user_id) in allowed_users:
        return True
    return False
