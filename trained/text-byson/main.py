# bot/main.py

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import telegram
import re

# load helper code
from helper import is_user
from palmai import palm_ai_instance  # Import the singleton instance from palmai.py

# Load environment variables
load_dotenv('/media/azzar/Betha/Download/project/telegram bot/yuna/yuna v1/chat mode/.env')

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
        send_chat_action(update, context, ChatAction.TYPING)

        # Generate a response using palmai.py
        response = palm_ai_instance.generate_response(user_input)

        # Send the response as a message
        send_message(update, context, response)
    else:
        message = f"Sorry, you are not authorized to use this bot."
        send_message(update, context, message)

def send_chat_action(update, context, action):
    """Send a chat action to indicate the bot's status."""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)

def send_message(update, context, message):
    # if no error (response)
    if message is not None:
        chunks = [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]
        for chunk in chunks:
            # Log the message content before sending
            print(f"Got response: {chunk}")
            chunk = re.sub(r"\bI am a large language model\b", "I am Yuna Ishikawa", chunk, flags=re.IGNORECASE)
            try:
                # Attempt to send the message with parse_mode="MARKDOWN"
                context.bot.send_message(chat_id=update.effective_chat.id, text=chunk, parse_mode="MARKDOWN")
            except telegram.error.BadRequest:
                # If there's a BadRequest error, send the message without parse_mode
                context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)
    # if error there is an error (null)
    if message is None:
        message = f"Sorry, An unexpected issue has arisen, but you can inquire about it at a later time if you wish."
        send_message(update, context, message)

# Function to handle the /help command
def help_command(update, context):
    logging.info(f"User selected the /help command")
    commands = [
        'here u can see the list of command that u can use on me 😊 :',
        '1. Bot Mode Changer 📳',
        '/createch - Enter Createch Mode.',
        '/research - Enter Researcher Assistant Mode.',
        '/paraphrasing - Enter Paraphrasing Mode.',
        '/iomutation - Enter IO Mutation Mode.',
        '/normal - Enter Normal Chat Mode.',
        '2. Question And Answer 🤓',
        '/detailed - Asking detailed answer',
        '/simple - Asking simple answer',
        '3. System Set ⚙️',
        '/start - Start Conversation with Yuna Ishikawa',
        '/reset - Reset Yuna Ishikawa for re-initialization.',
        '/help - show this help menu'
    ]
    send_chat_action(update, context, ChatAction.TYPING)
    message = "\n".join(commands)
    send_message(update, context, message)

# Function to handle the /start command
def start(update, context):
    logging.info(f"User selected the /start command")
    message = f"Hello, {update.message.from_user.first_name}! 🌟 I'm Yuna Ishikawa,\nyour very own AI chatbot powered by Palm 2 from Google. How may I be of service to you today? 💬 \nu can use \"/help\" to list all my command."
    send_message(update, context, message)

# Function to handle the /reset command
def reset(update, context):
    logging.info(f"User selected the /reset command")
    palm_ai_instance.reset()
    message = f"Yuna Ishikawa has been reset. You can now use \"/start\" to re-initialize me for a new conversation."
    send_message(update, context, message)

# Function to handle the /createch command
def createch(update, context):
    user_input = context.args  # This will be a list of words after the command
    if user_input:
        logging.info(f"User selected the /createch command with argument")
        user_input = ' '.join(user_input)  # Convert the list of words into a single string
        message = f"enter createch mode {user_input}"
    else:
        logging.info(f"User selected the /createch command")
        message = f"enter createch mode"

    send_chat_action(update, context, ChatAction.TYPING)
    response = palm_ai_instance.generate_response(message)
    send_message(update, context, response)

# Function to handle the /research command
def research(update, context):
    user_input = context.args  # This will be a list of words after the command
    if user_input:
        logging.info(f"User selected the /research command with argument")
        user_input = ' '.join(user_input)  # Convert the list of words into a single string
        message = f"enter researcher assistant mode {user_input}"
    else:
        logging.info(f"User selected the /research command")
        message = f"enter researcher assistant mode"

    send_chat_action(update, context, ChatAction.TYPING)
    response = palm_ai_instance.generate_response(message)
    send_message(update, context, response)

# Function to handle the /paraphrasing command
def paraphrasing(update, context):
    user_input = context.args  # This will be a list of words after the command
    if user_input:
        logging.info(f"User selected the /paraphrasing command with argument")
        user_input = ' '.join(user_input)  # Convert the list of words into a single string
        message = f"enter paraphrasing mode {user_input}"
    else:
        logging.info(f"User selected the /paraphrasing command")
        message = f"enter paraphrasing mode"

    send_chat_action(update, context, ChatAction.TYPING)
    response = palm_ai_instance.generate_response(message)
    send_message(update, context, response)

# Function to handle the /iomutation command
def iomutation(update, context):
    logging.info(f"User selected the /iomutation command")
    
    message = f"enter io mutation mode"
    send_chat_action(update, context, ChatAction.TYPING)
    response = palm_ai_instance.generate_response(message)
    send_message(update, context, response)

# Function to handle the /normal command
def normal(update, context):
    user_input = context.args  # This will be a list of words after the command
    if user_input:
        logging.info(f"User selected the /normal command with argument")
        user_input = ' '.join(user_input)  # Convert the list of words into a single string
        message = f"enter normal mode {user_input}"
    else:
        logging.info(f"User selected the /normal command")
        message = "enter normal mode"

    send_chat_action(update, context, ChatAction.TYPING)
    response = palm_ai_instance.generate_response(message)
    send_message(update, context, response)

# Function to handle the /detailed command
def detailed(update, context):
    user_input = context.args  # This will be a list of words after the command
    send_chat_action(update, context, ChatAction.TYPING)
    if user_input:
        logging.info(f"User selected the /detailed command with argument.")
        user_input = ' '.join(user_input)  # Convert the list of words into a single string
        message = f"give me a detailed possible answer about {user_input}"
        response = palm_ai_instance.generate_response(message)
        send_message(update, context, response)
    else:
        logging.info(f"User selected the /detailed command.")
        message = "please give your argument after the command, as \"/detailed\" + your argument"
        send_message(update, context, message)

# Function to handle the /simple command
def simple(update, context):
    user_input = context.args  # This will be a list of words after the command
    send_chat_action(update, context, ChatAction.TYPING)
    if user_input:
        logging.info(f"User selected the /simple command with argument.")
        user_input = ' '.join(user_input)  # Convert the list of words into a single string
        message = f"give me one simple possible answer (35 word max) about {user_input}"
        response = palm_ai_instance.generate_response(message)
        send_message(update, context, response)
    else:
        logging.info(f"User selected the /simple command")
        message = "please give your argument after the command, as \"/simple\" + your argument"
        send_message(update, context, message)

# Define command and message handlers
dp = dispatcher

dp.add_handler(CommandHandler("createch", createch))
dp.add_handler(CommandHandler("research", research))
dp.add_handler(CommandHandler("paraphrasing", paraphrasing))
dp.add_handler(CommandHandler("iomutation", iomutation))
dp.add_handler(CommandHandler("normal", normal))
dp.add_handler(CommandHandler("detailed", detailed))
dp.add_handler(CommandHandler("simple", simple))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("reset", reset))  
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: asyncio.run(process_input(update, context))))

# Start polling for updates
updater.start_polling()

# Log bot startup
logging.info("The bot has started")
logging.info("The bot is listening for messages")

# Keep the bot running
updater.idle()
