from django.http import HttpResponse, JsonResponse
from buyer.models import Email, ProfileBuyer, TokenEmail, TokenMain

import datetime
import hashlib
import smtplib

import jwt

from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD


class Auth:

    @staticmethod
    def user_register(user_data):
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            if ProfileBuyer.objects.filter(email=email).first():
                raise ValueError('the user is already registered')
        else:
            email = Email.objects.create(email=user_email)

            data_token = create_token()
            token = data_token['token']
            TokenEmail.objects.create(
                email=email,
                token_email=token,
                stop_date=data_token['stop_date'])

            password_hash = create_hash(user_data['password'])
            ProfileBuyer.objects.create(
                email=email,
                name=user_data['name'],
                surname=user_data['surname'],
                password=password_hash
            )

            send_notification([user_email], f'http://localhost/confirm/?token={token}')
        return HttpResponse(status=201)

    @staticmethod
    def user_repeat_notification(user_data):
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        activate = ProfileBuyer.objects.filter(email=email).first().active_account
        if not activate:
            data_token = create_token()
            token = data_token['token']
            if email:
                TokenEmail.objects.filter(email=email).update(
                    token_email=token,
                    stop_date=data_token['stop_date'])
                send_notification([user_email], f'http://localhost/confirm/?token={token}')
            else:
                raise ValueError('it is necessary to register')
        else:
            raise ValueError('The users email has been confirmed')
        return HttpResponse(status=201)

    @staticmethod
    def user_confirm_email(token):
        obj = TokenEmail.objects.filter(token_email=token).first().email
        stop_date = TokenEmail.objects.filter(token_email=token).first().stop_date
        now_date = datetime.datetime.now()
        if obj and stop_date.timestamp() > now_date.timestamp():
            ProfileBuyer.objects.filter(email=obj).update(active_account=True)
            return HttpResponse(status=201)
        else:
            raise ValueError('token is invalid')

    @staticmethod
    def user_login(user_data):
        user = Email.objects.filter(email=user_data['email']).first()
        if user:
            password_hash = create_hash(user_data['password'])
            if ProfileBuyer.objects.filter(email=user).first().password == password_hash:
                token_main = create_token()
                TokenMain.objects.create(
                    email=user,
                    token_main=token_main['token'],
                    stop_date=token_main['stop_date']
                )
                return JsonResponse(token_main['token'], status=200, safe=False)
            else:
                raise ValueError('invalid username or password')
        else:
            raise ValueError('user does not exist')


def create_token() -> dict:
    """
    JWT token generation
    :return: dict with a token and its expiration date, example {"token": "12345", "stop_date": 2023-12-27 10:37:08.84}
    """
    stop_date = datetime.datetime.now() + datetime.timedelta(hours=24)
    payload = {"sub": "admin", "exp": stop_date}
    return {'token': jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256"), 'stop_date': stop_date}


def create_hash(password) -> str:
    """
    Password hashing.
    :return: Hash of the string
    """
    salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()


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
