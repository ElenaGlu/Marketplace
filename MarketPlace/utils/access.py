import base64
import datetime
import hashlib
import json
import os
import smtplib

import jwt
from django.http import HttpResponse, JsonResponse

from buyer.models import Email, TokenBuyer
from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD
from seller.models import TokenSeller


def authentication_check(func):
    """
    Check of the user's primary authorization token.
    """

    def wrapper(*args):
        request = args[0]
        user_data = json.loads(request.body)
        token = user_data['token']
        if TokenBuyer.objects.filter(token=token).first():
            token_type = TokenBuyer
        else:
            token_type = TokenSeller
        stop_date = token_type.objects.filter(token=token).first().stop_date
        now_date = datetime.datetime.now()
        if stop_date.timestamp() > now_date.timestamp():
            profile = token_type.objects.filter(token=token).first().profile
        else:
            raise ValueError('the token is invalid, need to log in')
        del user_data['token']
        return func(profile, user_data)

    return wrapper


class Access:
    """
    Get access to the application.
    """

    @staticmethod
    def register(user_data, profile_type, email_token_type) -> None:
        """
        Registration of a new user in the system.
        :param user_data: dict containing keys - email, password, (name, surname,)
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :return: None
        :raises ValueError: if the user is registered in the system
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            if profile_type.objects.filter(email=email).first():
                raise ValueError('the user is already registered')
        else:
            user_data['email'] = Email.objects.create(email=user_email)

        user_data['password'] = Access.create_hash(user_data['password'])
        data_token = Access.create_token(profile_type.objects.create(**user_data))
        email_token_type.objects.create(**data_token)

        token = data_token['token']
        Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')

    @staticmethod
    def repeat_notification(user_data, profile_type, email_token_type) -> None:
        """
        Resend the email to the specified address.
        :param user_data: dict containing key - email
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :return: None
        :raises ValueError: if the user is not registered in the system
        :raises ValueError: if the user has already confirmed their profile
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            activate = profile_type.objects.filter(email=email).first().active_account
            if not activate:
                profile = profile_type.objects.filter(email=email).first()
                data_token = Access.create_token(profile)
                email_token_type.objects.filter(profile=profile).update(**data_token)

                token = data_token['token']
                Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')
            else:
                raise ValueError('The users email has been confirmed')
        else:
            raise ValueError('it is necessary to register')

    @staticmethod
    def confirm_email(token, profile_type, email_token_type) -> None:
        """
        Confirms the user's profile.
        :param token: string with token
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :return: None
        :raises ValueError: if the token has expired
        """
        obj = email_token_type.objects.filter(token=token).first().profile_id
        stop_date = email_token_type.objects.filter(token=token).first().stop_date
        now_date = datetime.datetime.now()
        if obj and stop_date.timestamp() > now_date.timestamp():
            profile_type.objects.filter(id=obj).update(active_account=True)
            email_token_type.objects.filter(token=token).first().delete()
        else:
            raise ValueError('token is invalid')

    @staticmethod
    def login(user_data, profile_type, token_type) -> str:
        """
        User authorization in the system.
        :param user_data: dict containing keys - email, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: object - TokenBuyer or TokenSeller
        :return: application access token
        :raises ValueError: if the user entered an incorrect email or password
        """
        email = Email.objects.filter(email=user_data['email']).first()
        user = profile_type.objects.filter(email=email).first()
        if user.active_account:
            password_hash = Access.create_hash(user_data['password'])
            if user.password == password_hash:
                data_token = Access.create_token(user)
                token_type.objects.create(**data_token)
                return data_token['token']
            else:
                raise ValueError('invalid username or password')
        else:
            raise ValueError('user does not exist')

    @staticmethod
    def redirect_reset(user_data, profile_type) -> None:
        """
        Sends a link to the email to reset the password
        :param user_data: dict containing key - email
        :param profile_type:  object - ProfileBuyer or ProfileSeller
        :return: None
        :raises ValueError: if the user entered an incorrect email
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            profile = profile_type.objects.filter(email=email).first()
            if profile:
                Access.send_notification([user_email], f'ссылка на форму')
            else:
                raise ValueError('user does not exist')
        else:
            raise ValueError('user does not exist')

    @staticmethod
    def reset_password(user_data, profile_type, token_type) -> None:
        """
        Changing the password to a new one
        :param user_data: dict containing keys - email, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: object - TokenBuyer or TokenSeller
        :return: None
        """
        email = Email.objects.filter(email=user_data['email']).first()
        profile = profile_type.objects.filter(email=email).first()
        token_type.objects.filter(profile=profile).delete()
        hash_password = Access.create_hash(user_data['password'])
        profile_type.objects.filter(email=email).update(password=hash_password)

    @staticmethod
    def logout(user_data, token_type) -> None:
        """
        Authorized user logs out of the system.
        :param user_data: dict containing key - token
        :param token_type: object - TokenBuyer or TokenSeller
        :return: None
        """
        token_type.objects.filter(token=user_data['token']).delete()

    @staticmethod
    def update_profile(profile, user_data, profile_type, token_type) -> HttpResponse:
        """
        Authorized user changes his profile data.
        :param profile: object ProfileBuyer
        :param user_data: dict containing keys - name, surname, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: object - TokenBuyer or TokenSeller
        :return:
        """
        if 'password' not in user_data:
            profile_type.objects.filter(id=profile.id).update(**user_data)
        else:
            user_data['password'] = Access.create_hash(user_data['password'])
            new_token = Access.create_token(profile)
            token_type.objects.filter(profile=profile.id).delete()
            token_type.objects.update(**new_token)

            profile_type.objects.filter(id=profile.id).update(**user_data, active_account=False)
            email = list(profile_type.objects.filter(id=profile.id).values('email'))[0]['email']
            email = list(Email.objects.filter(id=email).values('email'))[0]['email']

            Access.send_notification([email], f'')
            return JsonResponse(new_token['token'], status=201, safe=False)
        return HttpResponse(status=201)

    @staticmethod
    def create_token(profile_type) -> dict:
        """
        JWT token generation
        :return: dict with a token and its expiration date
        :return: example {"token": "12345", "stop_date": 2023-12-27 10:37:08.84}
        """
        stop_date = datetime.datetime.now() + datetime.timedelta(hours=24)
        payload = {"sub": "admin",
                   "exp": stop_date
                   }
        return {'profile': profile_type,
                'token': jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256"),
                'stop_date': stop_date
                }

    @staticmethod
    def create_hash(password, salt=os.urandom(32)) -> str:
        """
        Password hashing.
        :return: Hash of the string
        """
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        storage = salt + key
        return base64.b64encode(storage).decode('ascii').strip()


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
