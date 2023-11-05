# bot/helper.py

import os
import requests
from pydub import AudioSegment
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv('path_to_your_env_file')

class Helper:
    def is_user(self, user_id):
        allowed_users = os.getenv('USER_ID').split(',')
        return '*' in allowed_users or str(user_id) in allowed_users

    def is_admin(self, user_id):
        allowed_users = os.getenv('ADMIN_ID').split(',')
        return '*' in allowed_users or str(user_id) in allowed_users

    def translate_input(self, user_input):
        url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=en&q={user_input}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
        try:
            request_result = requests.get(url, headers=headers).json()
            translation = request_result[0][0]
            user_lang = request_result[0][1]
            return translation, user_lang
        except:
            return user_input, 'en'

    def translate_output(self, response, user_lang):
        if user_lang != 'en':
            url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=en&tl={user_lang}&q={response}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
            }
            try:
                request_result = requests.get(url, headers=headers).json()
                translation = request_result[0]
                return translation, user_lang
            except:
                return response, user_lang
        else:
            return response, user_lang

    def tts(self, last_response):
        if last_response[0] is not None:
            try:
                if last_response[1] is not None:
                    if last_response[1] != 'en':
                        user_lang = last_response[1]
                        text = last_response[0]
                        tts = gTTS(text=text, lang=user_lang, slow=False)
                    else:
                        text = last_response[0]
                        tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
                else:
                    text = last_response[0]
                    tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
            except:
                text = last_response[0]
                tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
        if last_response[0] is None:
            text = "There has been no response prior to this moment."
            tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
        tts.save('response.mp3')
        audio = AudioSegment.from_file("response.mp3", format="mp3")
        speedup = audio.speedup(playback_speed=1.22)
        speedup.export("voice.mp3", format="mp3")
        os.remove('response.mp3')

helper_code = Helper()
