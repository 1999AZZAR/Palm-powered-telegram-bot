# bot/helper.py

import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/media/azzar/Betha/Download/project/telegram bot/yuna/yuna v1 chat/.env')
            
def is_user(user_id):
    # Read the user IDs from .env file
    allowed_users = os.getenv('USER_ID').split(',')
    if str(user_id) in allowed_users:
        return True
    return False
