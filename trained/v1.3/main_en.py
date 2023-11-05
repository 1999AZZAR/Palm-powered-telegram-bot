# bot/main.py

import os
import logging
import telegram
import re

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# uncomment one to select the model
from helper_en import helper_code
# from helper_ja import helper_code

# uncomment one to select the model
from palmai_chat import palm_ai_instance
# from palmai_completion import palm_ai_instance

class BotHandler:
    def __init__(self):
        load_dotenv('path_to_your_env_file')
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.updater = Updater(self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.MAX_MESSAGE_LENGTH = 3048 # 4096 max
        self.palm_ai_instance = palm_ai_instance
        self.helper = helper_code
        self.user_last_responses = {}

    def run(self):
        self._add_command_handlers()
        self._add_message_handler()
        self.updater.start_polling()
        logging.info("The bot has started")
        logging.info("The bot is listening for messages")
        self.updater.idle()

    def _add_command_handlers(self):
        self.dispatcher.add_handler(CommandHandler("createch", self.createch))
        self.dispatcher.add_handler(CommandHandler("research", self.research))
        self.dispatcher.add_handler(CommandHandler("paraphrasing", self.paraphrasing))
        self.dispatcher.add_handler(CommandHandler("iomutation", self.iomutation))
        self.dispatcher.add_handler(CommandHandler("normal", self.normal))
        self.dispatcher.add_handler(CommandHandler("detailed", self.detailed))
        self.dispatcher.add_handler(CommandHandler("simple", self.simple))
        self.dispatcher.add_handler(CommandHandler("json", self.json))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("reset", self.reset))

    def _add_message_handler(self):
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.process_input))

    def process_input(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = update.message.text
            logging.info(f"got user input: {user_input}")
            translated_input = self.helper.translate_input(user_input)
            logging.info(f"translated input: {translated_input[0]}")
            user_input = translated_input[0]
            response = self.palm_ai_instance.generate_response(user_input)
            response = re.sub(r"\bI am a large language model\b", "I am Yuna Ishikawa", response, flags=re.IGNORECASE)
            message = self.helper.translate_output(response, f"{translated_input[1]}")
            self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def send_chat_action(self, update, context, action):
        """Send a chat action to indicate the bot's status."""
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)

    def send_message(self, update, context, message):
        self.send_chat_action(update, context, ChatAction.TYPING)
        user_id = update.message.from_user.id
        last_response = message
        logging.info(f"{last_response}")
        self.user_last_responses[user_id] = last_response 
        message = message[0]
        try:
            if message is not None:
                chunks = [message[i:i + self.MAX_MESSAGE_LENGTH] for i in range(0, len(message), self.MAX_MESSAGE_LENGTH)]
                for chunk in chunks:
                    try:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=chunk, parse_mode="MARKDOWN")
                    except telegram.error.BadRequest:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=chunk)
                if message is None:
                    message = [f"申し訳ありませんが、予期しない問題が発生しました。ご希望であれば、後で問い合わせることができます。"]
                    self.send_message(update, context, message)
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔊 ボイス", callback_data="tts")]])
            context.bot.send_message(chat_id=update.effective_chat.id, text="____", reply_markup=reply_markup)
        except:
            message = [f"申し訳ありませんが、予期しない問題が発生しました。ご希望であれば、後で問い合わせることができます。"]
            self.send_message(update, context, message)

        def button_click(update, context):
            query = update.callback_query
            user_id = query.from_user.id
            logging.info("asking for tts answer")
            if query.data == 'tts':
                if user_id in self.user_last_responses:
                    last_response = self.user_last_responses[user_id]
                    self.send_chat_action(update, context, ChatAction.RECORD_AUDIO)
                    self.helper.tts(last_response)
                    self.send_chat_action(update, context, ChatAction.UPLOAD_AUDIO)
                    context.bot.send_voice(chat_id=query.message.chat_id, voice=open('voice.mp3', 'rb'))
                    os.remove('voice.mp3')
                    logging.info("TTS done")
                else:
                    context.bot.send_message(chat_id=query.message.chat_id, text="No previous response to convert to TTS.")
            else:
                context.bot.send_message(chat_id=query.message.chat_id, text="Unknown button click.")
        self.dispatcher.add_handler(CallbackQueryHandler(button_click))

    def help_command(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_admin(user_id):
            logging.info(f"User selected the /help command")
            commands = [
                'here u can see the list of command that u can use on me 😊 :',
                '\n1. Bot Mode Changer 📳',
                '/createch - Enter Createch Mode.',
                '/research - Enter Researcher Assistant Mode.',
                '/paraphrasing - Enter Paraphrasing Mode.',
                '/iomutation - Enter IO Mutation Mode.',
                '/normal - Enter Normal Chat Mode.',
                '\n2. Question And Answer 🤓',
                '/detailed - Asking detailed answer',
                '/simple - Asking simple answer',
                '/json - Answer using json format',
                '\n3. System Set ⚙️',
                '/start - Start Conversation with Yuna Ishikawa',
                '/help - show this help menu',
                '/reset - Reset Yuna Ishikawa for re-initialization.'
            ]
            self.send_chat_action(update, context, ChatAction.TYPING)
            message = ["\n".join(commands)]
            self.send_message(update, context, message)
        elif self.helper.is_user(user_id):
            logging.info(f"User selected the /help command")
            commands = [
                'here u can see the list of command that u can use on me 😊 :',
                '\n1. Bot Mode Changer 📳',
                '/createch - Enter Createch Mode.',
                '/research - Enter Researcher Assistant Mode.',
                '/paraphrasing - Enter Paraphrasing Mode.',
                '/iomutation - Enter IO Mutation Mode.',
                '/normal - Enter Normal Chat Mode.',
                '\n2. Question And Answer 🤓',
                '/detailed - Asking detailed answer',
                '/simple - Asking simple answer',
                '\n3. System Set ⚙️',
                '/start - Start Conversation with Yuna Ishikawa',
                '/help - show this help menu'
            ]
            message = ["\n".join(commands)]
            self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def start(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            logging.info(f"User selected the /start command")
            message = [f"Hello {update.message.from_user.first_name}, I'm Yuna Ishikawa,\nyour very own AI chatbot powered by Palm 2 from Google. How may I be of service to you today? 💬 \nu can use \"/help\" to list all my command."]
            self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def reset(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_admin(user_id):
            logging.info(f"User selected the /reset command")
            self.palm_ai_instance.reset()
            message = [f"Yuna Ishikawa has been reset. You can now use \"/start\" to re-initialize me for a new conversation."]
            self.send_message(update, context, message)
        else:
            message = [f"Sorry, you are not authorized to use this command."]
            self.send_message(update, context, message)

    def createch(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /createch command with input: {user_input}")
                message = f"enter createch mode {user_input}"
            else:
                logging.info(f"User selected the /createch command")
                message = f"enter createch mode"
            message = [self.palm_ai_instance.generate_response(message)]
            self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def research(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /research command with input: {user_input}")
                command = f"enter researcher assistant mode:"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
                response = self.palm_ai_instance.generate_response(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
                self.send_message(update, context, message)
            else:
                logging.info(f"User selected the /research command")
                message = f"enter researcher assistant mode"
                message = [self.palm_ai_instance.generate_response(message)]
                self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def iomutation(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            logging.info(f"User selected the /iomutation command")
            message = f"enter io mutation mode"
            message = [self.palm_ai_instance.generate_response(message)]
            self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def normal(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /normal command with input: {user_input}")
                command = f"answer me using normal mode:"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
                response = self.palm_ai_instance.generate_response(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
                self.send_message(update, context, message)
            else:
                logging.info(f"User selected the /normal command")
                message = "enter normal mode"
                response = [self.palm_ai_instance.generate_response(message)]
                self.send_message(update, context, response)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def paraphrasing(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /paraphrasing command with input: {user_input}")
                command = f"paraphrase this for me:"
                message = f"{user_input}"
                translated_input = self.helper.translate_input(message)
                response = self.palm_ai_instance.generate_response(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
                self.send_message(update, context, message)
            else:
                logging.info(f"User selected the /paraphrasing command")
                message = f"enter paraphrasing mode"
                message = [self.palm_ai_instance.generate_response(message)]
                self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
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
                response = self.palm_ai_instance.generate_response(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
                self.send_message(update, context, message)
            else:
                logging.info(f"User selected the /detailed command.")
                message = ["please give your argument after the command, as \"/detailed\" + your argument"]
                self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
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
                response = self.palm_ai_instance.generate_response(message)
                translated_input = self.helper.translate_input(message)
                response = self.palm_ai_instance.generate_response(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
                self.send_message(update, context, message)
            else:
                logging.info(f"User selected the /simple command")
                message = ["please give your argument after the command, as \"/simple\" + your argument"]
                self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

    def json(self, update, context):
        user_id = update.message.from_user.id
        self.send_chat_action(update, context, ChatAction.TYPING)
        if self.helper.is_user(user_id):
            user_input = context.args
            if user_input:
                user_input = ' '.join(user_input)
                logging.info(f"User selected the /json command with input: {user_input}")
                command = f"answer me using json format only without any other explanation"
                message = f"{user_input}"
                response = self.palm_ai_instance.generate_response(message)
                translated_input = self.helper.translate_input(message)
                response = self.palm_ai_instance.generate_response(f"{command} + {translated_input[0]}")
                message = self.helper.translate_output(response, f"{translated_input[1]}")
                self.send_message(update, context, message)
            else:
                logging.info(f"User selected the /json command")
                message = ["please give your argument after the command, as \"/json\" + your argument"]
                self.send_message(update, context, message)
        else:
            message = [f"申し訳ありませんが、あなたには私を使用する権限がありません。"]
            self.send_message(update, context, message)

if __name__ == "__main__":
    bot_handler = BotHandler()
    bot_handler.run()
