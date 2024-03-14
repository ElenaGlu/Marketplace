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


TOKEN_USER_1 = os.getenv('TOKEN_USER_1')
TOKEN_USER_2 = os.getenv('TOKEN_USER_2')

TOKEN_USER_B = os.getenv('TOKEN_USER_B')
TOKEN_USER_S = os.getenv('TOKEN_USER_S')

TOKEN_MAIN_B = os.getenv('TOKEN_MAIN_B')


TOKEN_MAIN_4 = os.getenv('TOKEN_MAIN_4')
TOKEN_MAIN_B4 = os.getenv('TOKEN_MAIN_B4')

TOKEN_MAIN_S4 = os.getenv('TOKEN_MAIN_S4')
TOKEN_MAIN_S = os.getenv('TOKEN_MAIN_S')


VALID_TOKEN_B = os.getenv('VALID_TOKEN_B')
VALID_TOKEN_B4 = os.getenv('VALID_TOKEN_B4')

VALID_TOKEN_S = os.getenv('VALID_TOKEN_S')
VALID_TOKEN_S4 = os.getenv('VALID_TOKEN_S4')