# bot/palmai.py

import google.generativeai as palm
import os
from dotenv import load_dotenv

class PalmAI:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PalmAI, cls).__new__(cls)
            cls._instance._initialize_palm()
        return cls._instance

    def _initialize_palm(self):
        # Load credentials from a .env file
        load_dotenv('.env')

        # Read API key from the environment variable
        api_key = os.getenv('PALM_API_KEY')

        palm.configure(api_key=api_key)

        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        self.model = models[0].name

    def generate_response(self, user_input):
        """Generate a response based on user input using palm."""
        prompt = user_input

        completion = palm.generate_text(
            model=self.model,
            prompt=prompt,
            # The number of candidates to return
            candidate_count=8,
            # Set the temperature to 1.0 for more variety of responses.
            temperature=1.0,
            max_output_tokens=800,
        )

        return completion.result

    def reset(self):
        """Reset the PalmAI instance, allowing re-initialization."""
        self.__class__._instance = None

# Create a singleton instance of PalmAI 
palm_ai_instance = PalmAI()
