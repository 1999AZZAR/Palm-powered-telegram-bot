# bot/helper.py

import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv('path_to_your_env_file')

def is_user(user_id):
    # Read the user IDs from .env file
    allowed_users = os.getenv('USER_ID').split(',')
    
    # Check if '*' is in allowed_users
    if '*' in allowed_users:
        return True
    
    # Check if the user_id is in the allowed_users list
    if str(user_id) in allowed_users:
        return True
    
    return False
