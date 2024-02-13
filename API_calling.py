from openai import OpenAI
import json
from openai.types.beta import Assistant
from dotenv import load_dotenv, find_dotenv


_ : bool = load_dotenv(find_dotenv()) # read local .env file
client : OpenAI = OpenAI()


