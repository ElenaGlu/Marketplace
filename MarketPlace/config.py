import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

KEY_NAME = os.getenv('KEY_NAME')
KEY_USER = os.getenv('KEY_USER')
KEY_PASSWORD = os.getenv('KEY_PASSWORD')

KEY_SENDER = os.getenv('KEY_SENDER')
KEY_SENDER_PASSWORD = os.getenv('KEY_SENDER_PASSWORD')

EMAIL_1 = os.getenv('EMAIL_1')
EMAIL_2 = os.getenv('EMAIL_2')
EMAIL_3 = os.getenv('EMAIL_3')
EMAIL_4 = os.getenv('EMAIL_4')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

