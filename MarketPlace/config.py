import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

KEY_SENDER = os.getenv('KEY_SENDER')
KEY_SENDER_PASSWORD = os.getenv('KEY_SENDER_PASSWORD')

EMAIL_1 = os.getenv('EMAIL_1')
EMAIL_2 = os.getenv('EMAIL_2')
EMAIL_3 = os.getenv('EMAIL_3')
EMAIL_4 = os.getenv('EMAIL_4')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

TOKEN_EMAIL_BUYER = os.getenv('TOKEN_EMAIL_BUYER')  # confirm email
TOKEN_EMAIL_B = os.getenv('TOKEN_EMAIL_B')
TOKEN_EMAIL_SELLER = os.getenv('TOKEN_EMAIL_SELLER')
TOKEN_EMAIL_S = os.getenv('TOKEN_EMAIL_S')

TOKEN_SH310 = os.getenv('TOKEN_SH310')  # reset sh310 del

TOKEN_BUYER = os.getenv('TOKEN_BUYER')
TOKEN_B = os.getenv('TOKEN_B')  # logout del

TOKEN_SELLER = os.getenv('TOKEN_SELLER')  # logout del
TOKEN_S = os.getenv('TOKEN_S')

VALID_TOKEN_BUYER = os.getenv('VALID_TOKEN_BUYER')  # reset pwd del all
VALID_TOKEN_B = os.getenv('VALID_TOKEN_B')

VALID_TOKEN_SELLER = os.getenv('VALID_TOKEN_SELLER')  # reset pwd del all
VALID_TOKEN_S = os.getenv('VALID_TOKEN_S')

TOKEN_SHOP_BUYER = os.getenv('TOKEN_SHOP_BUYER')  # active token for shop
TOKEN_SHOP_B = os.getenv('TOKEN_SHOP_B')

TOKEN_SHOP_SELLER = os.getenv('TOKEN_SHOP_SELLER')  # active token for shop
TOKEN_SHOP_S = os.getenv('TOKEN_SHOP_S')

TOKEN_UPDATE_PROFILE_B = os.getenv('TOKEN_UPDATE_PROFILE_B')   # active token for update profile
TOKEN_UPDATE_B = os.getenv('TOKEN_UPDATE_B')

TOKEN_UPDATE_PROFILE_S = os.getenv('TOKEN_UPDATE_PROFILE_S')  # active token for update profile
TOKEN_UPDATE_S = os.getenv('TOKEN_UPDATE_S')
