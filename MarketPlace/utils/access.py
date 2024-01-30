import datetime

import hashlib
import json
import smtplib
import jwt

from django.http import HttpResponse, JsonResponse

from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD
from buyer.models import Email, TokenEmail, TokenMain


def decorator_authentication(func):
    """
    Token validation.
    """

    def wrapper(*args):
        request = args[0]
        token = json.loads(request.body)['token']
        stop_date = TokenMain.objects.filter(token=token).first().stop_date
        now_date = datetime.datetime.now()
        if stop_date.timestamp() > now_date.timestamp():
            email = TokenMain.objects.filter(token=token).first().email
        else:
            raise ValueError('the token is invalid, need to log in')
        return func(email, request)

    return wrapper


class Access:
    """
    Get access to the application.
    """

    @staticmethod
    def register(user_data, profile_type) -> HttpResponse:
        """
        Registration of a new user in the system.
        :param profile_type: object - buyer or seller
        :param user_data: a dictionary containing keys: email, password..
        :return: "created" (201) response code
        :raises ValueError: if the user is registered in the system
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            if profile_type.objects.filter(email=email).first():
                raise ValueError('the user is already registered')
        else:
            email = Email.objects.create(email=user_email)

        data_token = Access.create_token(email)
        TokenEmail.objects.create(**data_token)

        user_data['password'] = Access.create_hash(user_data['password'])
        user_data['email'] = email
        profile_type.objects.create(**user_data)

        token = data_token['token']
        Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')
        return HttpResponse(status=201)

    @staticmethod
    def repeat_notification(user_data, profile_type) -> HttpResponse:
        """
        Resend the email to the specified address.
        :param profile_type: object - buyer or seller
        :param user_data: a dictionary containing key: email
        :return: "created" (201) response code
        :raises ValueError: if the user is not registered in the system
        :raises ValueError: if the user has already confirmed their profile
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            activate = profile_type.objects.filter(email=email).first().active_account
            if not activate:
                data_token = Access.create_token(email)
                TokenEmail.objects.filter(email=email).update(**data_token)

                token = data_token['token']
                Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')
            else:
                raise ValueError('The users email has been confirmed')
        else:
            raise ValueError('it is necessary to register')
        return HttpResponse(status=201)

    @staticmethod
    def confirm_email(token, profile_type) -> HttpResponse:
        """
        Confirms the user's profile.
        :param profile_type: object - buyer or seller
        :param token: a dictionary containing key: token
        :return: "created" (201) response code
        :raises ValueError: if the token has expired
        """
        obj = TokenEmail.objects.filter(token=token).first().email
        stop_date = TokenEmail.objects.filter(token=token).first().stop_date
        now_date = datetime.datetime.now()
        if obj and stop_date.timestamp() > now_date.timestamp():
            profile_type.objects.filter(email=obj).update(active_account=True)
            return HttpResponse(status=201)
        else:
            raise ValueError('token is invalid')

    @staticmethod
    def login(user_data, profile_type) -> JsonResponse:
        """
        User authorization in the system.
        :param profile_type:  object - buyer or seller
        :param user_data: dictionary containing keys: email, password
        :return: application access token
        :raises ValueError: if the user entered an incorrect email or password
        """
        email = Email.objects.filter(email=user_data['email']).first()
        if email:
            password_hash = Access.create_hash(user_data['password'])
            if profile_type.objects.filter(email=email).first().password == password_hash:
                token_main = Access.create_token(email)
                TokenMain.objects.create(**token_main)
                return JsonResponse(token_main['token'], status=200, safe=False)
            else:
                raise ValueError('invalid username or password')
        else:
            raise ValueError('user does not exist')

    @staticmethod
    def create_token(email) -> dict:
        """
        JWT token generation
        :return: dict with a token and its expiration date, example {"token": "12345", "stop_date": 2023-12-27 10:37:08.84}
        """
        stop_date = datetime.datetime.now() + datetime.timedelta(hours=24)
        payload = {"sub": "admin", "exp": stop_date}
        return {'email': email,
                'token': jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256"),
                'stop_date': stop_date
                }

    @staticmethod
    def create_hash(password) -> str:
        """
        Password hashing.
        :return: Hash of the string
        """
        salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

    @staticmethod
    def send_notification(email, txt) -> None:
        """
        Sends an email to the specified address.
        """
        sender = KEY_SENDER
        sender_password = KEY_SENDER_PASSWORD
        mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        mail_lib.login(sender, sender_password)

        for to_item in email:
            msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
                sender, to_item, 'confirm')
            msg += txt
            mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
        mail_lib.quit()
