# bot/main.py

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import telegram
import re


from helper import is_user
#from palmai import generate_response  # Import the function from palmai.py
from palmai import palm_ai_instance  # Import the singleton instance from palmai.py


# Load environment variables
load_dotenv('.env')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Retrieve the bot token from environment variables
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

# Initialize the Telegram Updater with context
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# Maximum message length for splitting
MAX_MESSAGE_LENGTH = 4096

async def process_input(update, context):
    """Process user input and generate a response using palmai.py."""
    user_id = update.message.from_user.id

    if is_user(user_id):
        user_input = update.message.text

        # Log the message content before sending
        print(f"Sending message: {user_input}")

        # Send "typing..." status
        await send_chat_action(update, context, ChatAction.TYPING)

        # Generate a response using palmai.py
        response = palm_ai_instance.generate_response(user_input)

        # Send the response as a message
        send_message(update, context, response)
    else:
        message = 'Sorry, you are not authorized to use this bot.'
        send_message(update, context, message)

async def send_chat_action(update, context, action):
    """Send a chat action to indicate the bot's status."""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)

def send_message(update, context, message):
    chunks = [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]

    for chunk in chunks:
        # Log the message content before sending
        print(f"Got response: {chunk}")
        chunk = re.sub(r'\bPalm ai\b', 'yuna ishikawa', chunk, flags=re.IGNORECASE)

        try:
            # Attempt to send the message with parse_mode="MARKDOWN"
            context.bot.send_message(chat_id=update.effective_chat.id, text=chunk, parse_mode="MARKDOWN")
        except telegram.error.BadRequest:
            # If there's a BadRequest error, send the message without parse_mode
            context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)

def start(update, context):
    """Send a message when the command /start is issued."""
    message = 'Hi! I am yuna, your personal AI-powered chatbot. How can I assist you today?'
    send_message(update, context, message)
    
def reset(update, context):
    """Reset the PalmAI instance for re-initialization."""
    palm_ai_instance.reset()
    message = 'yuna ishikawa has been reset. You can now re-initialize me for a new conversation.'
    send_message(update, context, message)

# Define command and message handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("reset", reset))  # Add a reset command handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: asyncio.run(process_input(update, context))))

# Start polling for updates
updater.start_polling()

# Log bot startup
logging.info("The bot has started")
logging.info("The bot is listening for messages")

# Keep the bot running
updater.idle()
