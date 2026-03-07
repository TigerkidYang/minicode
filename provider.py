import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMProvider:

    def __init__(self):

        # Load the API key from environment variables
        api_key = os.getenv("OPENROUTER_API_KEY")

        # Initialize the OpenAI client with the API key
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        # Model
        self.default_model = "google/gemini-3-flash-preview"

    def chat(self, messages : list, tools : list = None):

        # Parameters
        api_params = {
            "model" : self.default_model,
            "messages" : messages,
            "temperature" : 0.1,
        }

        # Pass tools if tools
        if tools:
            api_params["tools"] = tools

        # Ask for response
        response = self.client.chat.completions.create(**api_params)

        # Return the core response
        return response.choices[0].message
