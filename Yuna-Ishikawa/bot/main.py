# bot/main.py

import os
import logging
import telegram
import threading
import time
import html
import re

from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import NetworkError

from helper import helper_code
from palmai import palm_instance
from datamanager import DatabaseManager

class BotHandler:
    connection_alive = True 

    def __init__(self):
        load_dotenv('.env')
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.updater = Updater(self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self._add_CallbackQueryHandler()
        self.MAX_MESSAGE_LENGTH = 2048 # 4096 max
        self.palm_instance = palm_instance
        self.db_manager = DatabaseManager()
        self.helper = helper_code
        self.user_last_responses = {}

    def _add_command_handlers(self):
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("reset", self.reset))
        self.dispatcher.add_handler(CommandHandler("detailed", self.detailed))
        self.dispatcher.add_handler(CommandHandler("simple", self.simple))
        self.dispatcher.add_handler(CommandHandler("paraphrase", self.paraphrase))
        self.dispatcher.add_handler(CommandHandler("summarize", self.summarize))
        self.dispatcher.add_handler(CommandHandler("elaborate", self.elaborate))
    
    def _add_CallbackQueryHandler(self):
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_click))

    def _add_message_handler(self):
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.process_input))

    def run(self):
            self._add_command_handlers()
            self._add_message_handler()
            self.updater.start_polling()
            logging.info("The bot has started")
            logging.info("The bot is listening for messages")
            threading.Thread(target=self.connection_watchdog, daemon=True).start()
            self.updater.idle()

    def connection_watchdog(self):
        while True:
            try:
                self.updater.bot.get_me()
                if not self.connection_alive:
                    logging.info("Connection reestablished.")
                    self.connection_alive = True
            except NetworkError:
                if self.connection_alive:
                    logging.error("Connection lost. Attempting to reconnect...")
                    self.connection_alive = False
                    self.updater.start_polling(drop_pending_updates=True)
            time.sleep(10)

    def process_input(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = update.message.text
            user_input = html.escape(user_input)
            logging.info(f"got {update.message.from_user.first_name} as user with id {user_id}, input: {user_input}")
            translated_input = self.helper.translate_input(user_input)
            # logging.info(f"translated input: {translated_input[0]}")
            user_input = translated_input[0]
            response = self.palm_instance.generate_chat(user_input)
            response = re.sub(r"\bI am a large language model\b", "my name is Yuna Ishikawa", response, flags=re.IGNORECASE)
            message = self.helper.translate_output(response, f"{translated_input[1]}")
        else:
            message = [f"Apologies, you lack the necessary authorization to utilize my services."]
        self.send_message(update, context, message)

    def send_chat_action(self, update, context, action):
        """Send a chat action to indicate the bot's status."""
        try:
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
        except telegram.error.TimedOut:
            logging.error("Timed out while sending chat action. Ignoring and continuing.")

    def send_message(self, update, context, message):
        self.send_chat_action(update, context, ChatAction.TYPING)
        user_id = (update.callback_query.from_user.id if update.callback_query and update.callback_query.from_user else None) or (update.message.from_user.id if update.message and update.message.from_user else None)
        response = message[0]
        lang = message[1]
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d%m%y%H%M%S")
        data_id = int(formatted_time)
        logging.info(f"Storing user data")
        self.db_manager.store_user_data(user_id, data_id, response, lang)
        logging.info(f"Sending response: {message}")
        try:
            if response is not None:
                chunks = [response[i:i + self.MAX_MESSAGE_LENGTH] for i in range(0, len(response), self.MAX_MESSAGE_LENGTH)]
                for index, chunk in enumerate(chunks):
                    if index == len(chunks) - 1:
                        reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("🔊 voice", callback_data=f"tts_{data_id}"),
                                    InlineKeyboardButton("📝 elaborate", callback_data=f"elaborate_{data_id}"),
                                ],
                                [
                                    InlineKeyboardButton("🗞️ summary", callback_data=f"summarize_{data_id}"),
                                    InlineKeyboardButton("✍🏻 paraphrase", callback_data=f"paraphrase_{data_id}"),
                                ],
                            ]
                        )
                    else:
                        reply_markup = None
                    try:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=chunk, parse_mode="MARKDOWN", reply_markup=reply_markup)
                    except telegram.error.BadRequest:
                        chunk = html.escape(chunk)
                        context.bot.send_message(chat_id=update.effective_chat.id, text=chunk, reply_markup=reply_markup)
            if response is None:
                message = (f"I'm sorry, but an unexpected problem has occurred. If you wish, you can try again later.",'en')
                self.send_message(update, context, message)
        except:
            message = (f"there has been no response at the moment",'en')
            self.send_message(update, context, message)

    def button_click(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id if query.from_user else None

        if user_id is not None:
            callback_data_parts = query.data.split("_")
            if len(callback_data_parts) == 2 :
                data_id = int(callback_data_parts[1])
                logging.info(f"User {user_id} clicked the button for data_id {data_id}")
                response_text = self.db_manager.retrieve_user_data_by_data_id(user_id, data_id)
                self.user_last_responses[user_id] = response_text
                if callback_data_parts[0] == 'tts':
                    if response_text:
                        self.send_chat_action(update, context, ChatAction.RECORD_AUDIO)
                        self.helper.tts(response_text)
                        self.send_chat_action(update, context, ChatAction.UPLOAD_AUDIO)
                        context.bot.send_voice(chat_id=query.message.chat_id, voice=open('voice.mp3', 'rb'))
                        os.remove('voice.mp3')
                        logging.info("TTS done")
                    else:
                        message = (f"Could not find response for data_id {data_id}", 'en')
                        self.send_chat_action(update, context, ChatAction.TYPING)
                        time.sleep(1)
                        self.send_message(update, context, message)
                elif callback_data_parts[0] == 'summarize':
                    logging.info("asking for summarization answer")
                    self.summarize(update, context)
                elif callback_data_parts[0] == 'paraphrase':
                    logging.info("asking for paraphrased answer")
                    self.paraphrase(update, context)
                elif callback_data_parts[0] == 'elaborate':
                    logging.info("asking for elaborated answer")
                    self.elaborate(update, context)
        else:
            message = (f"User information not available.", 'en')
            self.send_chat_action(update, context, ChatAction.TYPING)
            time.sleep(1)
            self.send_message(update, context, message)

    def help_command(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            logging.info(f"User selected the /help command")
            commands = [
                'here u can see the list of command that u can use on me 😊 :',
                '\n1. Operation mode 📳',
                '/paraphrase - Paraphrase your input or my latest response.',
                '/summarize  - summarize your input or my latest response.',
                '/elaborate  - elaborate your input or my latest response.',
                '\n2. Question And Answer 🤓',
                '/detailed - Asking me for a detailed answer',
                '/simple   - Asking me for a simple answer',
                '\n3. System Set ⚙️',
                '/start - Start Conversation with me',
                '/help  - show this help menu',
                '/reset - Reset me for re-initialization.'
            ]
            self.send_chat_action(update, context, ChatAction.TYPING)
            message = ("\n".join(commands),'en')
        else:
            message = (f"Apologies, you lack the necessary authorization to utilize my services.",'en')
        self.send_message(update, context, message)

    def start(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            logging.info(f"User selected the /start command")
            message = (f"Hello {update.message.from_user.first_name}, I'm Yuna Ishikawa,\nyour very own AI chatbot powered by Palm 2 from Google. How may I be of service to you today? 💬 \nu can use \"/help\" to list all my command.",'en')
            self.send_message(update, context, message)
        else:
            message = (f"Apologies, you lack the necessary authorization to utilize my services.",'en')
            self.send_message(update, context, message)

    def reset(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_admin(user_id):
            logging.info(f"User selected the /reset command")
            self.palm_instance.reset()
            message = (f"Yuna Ishikawa has been reset. You can now use \"/start\" to re-initialize me for a new conversation.",'en')
        else:
            message = (f"Apologies, but access to this command is restricted to administrators only.",'en')
        self.send_message(update, context, message)

    def summarize(self, update, context):
        user_id = (update.callback_query.from_user.id if update.callback_query and update.callback_query.from_user else None) or (update.message.from_user.id if update.message and update.message.from_user else None)
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /summarize command with input: {user_input}")
                command = f"summarize this for me make it more simple and shorter but understandable:"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
            else:
                command = f"summarize this for me make it more simple and shorter but understandable:"
                message = self.user_last_responses[user_id]
                translated_input = self.helper.translate_input({message})
            response = self.palm_instance.generate_text(f"{command} + {translated_input[0]}")
            message = self.helper.translate_output(response, f"{translated_input[1]}")        
        else:
            message = (f"Sorry, you are not authorized for using this feature",'en')
        self.send_message(update, context, message)

    def paraphrase(self, update, context):
        user_id = (update.callback_query.from_user.id if update.callback_query and update.callback_query.from_user else None) or (update.message.from_user.id if update.message and update.message.from_user else None)
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /paraphrasing command with input: {user_input}")
                command = f"paraphrase the following text by proofreading, rewording, and/or rephrasing it. I'm looking for a refined version that maintains clarity and coherence.:"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
            else:
                command = f"paraphrase the following text by proofreading, rewording, and/or rephrasing it. I'm looking for a refined version that maintains clarity and coherence.:"
                message = self.user_last_responses[user_id]
                translated_input = self.helper.translate_input({message})
            response = self.palm_instance.generate_text(f"{command} + {translated_input[0]}")
            message = self.helper.translate_output(response, f"{translated_input[1]}") 
        else:
            message = (f"Apologies, you lack the necessary authorization to utilize my services.",'en')
        self.send_message(update, context, message)

    def elaborate(self, update, context):
        user_id = (update.callback_query.from_user.id if update.callback_query and update.callback_query.from_user else None) or (update.message.from_user.id if update.message and update.message.from_user else None)
        self.send_chat_action(update, context, ChatAction.TYPING)
        logging.info(f"user using the /elaborate command")
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /elaborate command with input: {user_input}")
                command = f"Elaborate this make it longer by provide more details, but ensure it remains understandable.:"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
            else:
                command = f"Elaborate this make it longer by provide more details, but ensure it remains understandable.:"
                message = self.user_last_responses[user_id]
                translated_input = self.helper.translate_input({message})
            response = self.palm_instance.generate_text(f"{command} + {translated_input[0]}")
            message = self.helper.translate_output(response, f"{translated_input[1]}")        
        else:
            message = (f"Sorry, you are not authorized for using this feature",'en')
        self.send_message(update, context, message)

    def detailed(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /detailed command with input: {user_input}")
                command = f"give me a detailed possible answer or explanation about"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
                response = self.palm_instance.generate_chat(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
            else:
                message = (f"please give your argument after the command, as \"/detailed\" + your argument",'en')
        else:
            message = (f"Apologies, you lack the necessary authorization to utilize my services.",'en')
        self.send_message(update, context, message)

    def simple(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /simple command with input: {user_input}")
                command = f"give me one simple possible answer or explanation (35 word max) about"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
                response = self.palm_instance.generate_chat(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
            else:
                message = (f"please give your argument after the command, as \"/simple\" + your argument",'en')
        else:
            message = (f"Apologies, you lack the necessary authorization to utilize my services.",'en')
        self.send_message(update, context, message)

if __name__ == "__main__":
    bot_handler = BotHandler()
    bot_handler.run()
