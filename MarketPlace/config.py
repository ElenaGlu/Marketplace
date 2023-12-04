import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

KEY_NAME = os.getenv('KEY_NAME')
KEY_USER = os.getenv('KEY_USER')
KEY_PASSWORD = os.getenv('KEY_PASSWORD')