import base64
import datetime
import hashlib
import json
import os
import smtplib
from typing import Dict, Type

import jwt
from django.http import HttpRequest

from Exceptions import AppError, ErrorType
from buyer.models import Email
from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD, REDIS_HOST, REDIS_PORT

import redis

user_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


def authentication_check(token_type: str):
    """
    Check of the user's primary authorization token.
    :param token_type: 'TokenBuyer' or 'TokenSeller'
    """

    def decorator_auth_check(func):

        def wrapper_auth_check(request: HttpRequest):
            user_data = json.loads(request.body)
            token_user = user_connection.keys(pattern=f"*:{token_type}:{user_data['token']}")[0]
            if token_user:
                profile_id = int(token_user.split(":")[0])
                del user_data['token']
                return func(profile_id, user_data)
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.TOKEN_ERROR,
                        'description': 'the token is invalid, need to log in'
                    }
                )

        return wrapper_auth_check

    return decorator_auth_check


class Access:
    """
    Get access to the application.
    """

    @staticmethod
    def register(user_data: Dict[str, str], profile_type: Type, token_email_type: str) -> None:
        """
        Registration of a new user in the system.
        :param user_data: dict containing keys - email, password, (name, surname,)
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_email_type: 'TokenEmailBuyer' or 'TokenEmailSeller'
        :return: None
        :raises AppError: if the user is registered in the system
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            if profile_type.objects.filter(email=email).first():
                raise AppError(
                    {
                        'error_type': ErrorType.REGISTRATION_ERROR,
                        'description': 'User is already registered'
                    }
                )
        else:
            user_data['email'] = Email.objects.create(email=user_email)

        user_data['password'] = Access.create_hash(user_data['password'])
        new_user = profile_type.objects.create(**user_data).id
        data_token = Access.redis_create_token(new_user, token_email_type)
        user_connection.setex(data_token, 86400, '')
        token = data_token.split(":")[2]
        Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')

    @staticmethod
    def repeat_notification(user_data: Dict[str, str], profile_type: Type, token_email_type: str) -> None:
        """
        Resend the email to the specified address.
        :param user_data: dict containing key - email
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_email_type: 'TokenEmailBuyer' or 'TokenEmailSeller'
        :return: None
        :raises AppError: if the user is not registered in the system
        :raises AppError: if the user has already confirmed their profile
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            activate = profile_type.objects.filter(email=email).first().active_account
            if not activate:
                profile = profile_type.objects.filter(email=email).first().id
                data_token = Access.redis_create_token(profile, token_email_type)
                user_connection.setex(data_token, 86400, '')
                token = data_token.split(":")[2]
                Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.REGISTRATION_ERROR,
                        'description': 'The users email has been confirmed'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.REGISTRATION_ERROR,
                    'description': 'User is not registered.It is necessary to register'
                }
            )

    @staticmethod
    def confirm_email(token: str, profile_type: Type, token_email_type: str) -> None:
        """
        Confirms the user's profile.
        :param token: string with token
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_email_type: 'TokenEmailBuyer' or 'TokenEmailSeller'
        :return: None
        :raises AppError: if email token is invalid
        """
        token_user = user_connection.keys(pattern=f"*:{token_email_type}:{token}")[0]
        if token_user:
            id_user = token_user.split(":")
            profile_type.objects.filter(id=id_user[0]).update(active_account=True)
        else:
            raise AppError(
                {
                    'error_type': ErrorType.EMAIL_TOKEN_ERROR,
                    'description': 'Email token is invalid'
                }
            )

    @staticmethod
    def login(user_data: Dict[str, str], profile_type: Type, token_type: str) -> str:
        """
        User authorization in the system.
        :param user_data: dict containing keys - email, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: 'TokenBuyer' or 'TokenSeller'
        :return: application access token
        :raises AppError: if the user entered an incorrect email or password
        :raises AppError: if the user's account has not been activated
        :raises AppError: if the user is not registered
        """
        email = Email.objects.filter(email=user_data['email']).first()
        if email:
            user = profile_type.objects.filter(email=email).first()
            if user.active_account:
                password_hash = Access.create_hash(user_data['password'])
                if user.password == password_hash:
                    data_token = Access.redis_create_token(user.id, token_type)
                    user_connection.setex(data_token, 2419200, '')
                    return data_token.split(":")[2]
                else:
                    raise AppError(
                        {
                            'error_type': ErrorType.ACCESS_ERROR,
                            'description': 'Invalid email or password'
                        }
                    )
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.REGISTRATION_ERROR,
                        'description': 'The users account has not been activated. Confirm your email'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.REGISTRATION_ERROR,
                    'description': 'User is not registered.It is necessary to register'
                }
            )

    @staticmethod
    def redirect_reset(user_data: Dict[str, str], profile_type: Type) -> None:
        """
        Sends a link to the email to reset the password
        :param user_data: dict containing key - email
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :return: None
        :raises AppError: if user is not registered
        """
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            profile = profile_type.objects.filter(email=email).first()
            if profile:
                Access.send_notification([user_email], f'link to the password change form')
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.REGISTRATION_ERROR,
                        'description': 'User is not registered.It is necessary to register'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.REGISTRATION_ERROR,
                    'description': 'User is not registered.It is necessary to register'
                }
            )

    @staticmethod
    def reset_password(user_data: Dict[str, str], profile_type: Type, token_type: str) -> None:
        """
        Changing the password to a new one
        :param user_data: dict containing keys - email, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: 'TokenBuyer' or 'TokenSeller'
        :return: None
        :raises AppError: if user is not registered
        """
        email = Email.objects.filter(email=user_data['email']).first()
        if email:
            profile = profile_type.objects.filter(email=email).first().id
            if profile:
                for key in user_connection.scan_iter(f"{profile}:{token_type}:*"):
                    user_connection.delete(key)
                hash_password = Access.create_hash(user_data['password'])
                profile_type.objects.filter(email=email).update(password=hash_password, active_account=True)
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.REGISTRATION_ERROR,
                        'description': 'User is not registered.It is necessary to register'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.REGISTRATION_ERROR,
                    'description': 'User is not registered.It is necessary to register'
                }
            )

    @staticmethod
    def logout(user_data: Dict[str, str], token_type: str) -> None:
        """
        Authorized user logs out of the system.
        :param user_data: dict containing key - token
        :param token_type: 'TokenBuyer' or 'TokenSeller'
        :return: None
        """
        user_connection.delete(f"*:{token_type}:{user_data['token']}")

    @staticmethod
    def update_profile(
            profile_id: int,
            user_data: Dict[str, str],
            profile_type: Type,
            token_type: str
    ) -> None:
        """
        Authorized user changes his profile data.
        :param profile_id: ProfileBuyer's id or ProfileSeller's id
        :param user_data: dict containing keys - name, surname, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: 'TokenBuyer' or 'TokenSeller'
        :return: None
        """
        user = profile_type.objects.filter(id=profile_id)
        if 'password' not in user_data:
            user.update(**user_data)
        else:
            user_data['password'] = Access.create_hash(user_data['password'])
            for key in user_connection.scan_iter(f"{profile_id}:{token_type}:*"):
                user_connection.delete(key)
            user.update(**user_data, active_account=False)

            new_token = Access.redis_create_token(profile_id, f"{token_type}:update")
            user_connection.setex(new_token, 86400, '')
            token = new_token.split(":")[2]

            email = list(user.values('email'))[0]['email']
            email = list(Email.objects.filter(id=email).values('email'))[0]['email']
            Access.send_notification([email], f'http://localhost/update/?token={token}')

    @staticmethod
    def update_pwd(token: str, profile_type: Type, token_type: str) -> None:
        """
        Confirms the user's profile.
        :param token: string with token
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: 'ProfileBuyer' or 'ProfileBuyer'
        :return: None
        :raises AppError: if token is invalid
        """
        token_user = user_connection.keys(pattern=f"*:{token_type}:update:{token}")[0]
        if token_user:
            id_user = token_user.split(":")
            profile_type.objects.filter(id=id_user[0]).update(active_account=True)
            user_connection.delete(token_user)
        else:
            raise AppError(
                {
                    'error_type': ErrorType.EMAIL_TOKEN_ERROR,
                    'description': 'The token is invalid'
                }
            )

    @staticmethod
    def redis_create_token(id_user, token_type):
        """
        The function is under revision.
        """
        payload = {"sub": "admin",
                   "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
                   }
        token = jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256")
        return f"{id_user}:{token_type}:{token}"

    @staticmethod
    def create_hash(password: str, salt=os.urandom(32)) -> str:
        """
        Password hashing.
        :param password: str
        :param salt: random bytes
        :return: Hash of the string
        """
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        storage = salt + key
        return base64.b64encode(storage).decode('ascii').strip()

    @staticmethod
    def send_notification(email: list[str], txt: str) -> None:
        """
        Sends an email to the specified address.
        :param email: user's address
        :param txt: message that will be sent to the user
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
