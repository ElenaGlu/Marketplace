import base64
import datetime
import hashlib
import json
import os
import smtplib
from typing import Dict, Type, Union, Optional

import jwt
from django.http import HttpRequest

from Exceptions import AppError, ErrorType
from buyer.models import Email, TokenBuyer
from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD
from seller.models import TokenSeller


def authentication_check(func):
    """
    Check of the user's primary authorization token.
    """

    def wrapper(request: HttpRequest):
        user_data = json.loads(request.body)
        token = user_data['token']
        if TokenBuyer.objects.filter(token=token).first():
            token_type = TokenBuyer
        elif TokenSeller.objects.filter(token=token).first():
            token_type = TokenSeller
        else:
            raise AppError(
                {
                    'error_type': ErrorType.TOKEN_ERROR,
                    'description': 'the token is invalid, need to log in'
                }
            )
        token_data = token_type.objects.filter(token=token).first()
        stop_date = token_data.stop_date
        now_date = datetime.datetime.now(datetime.timezone.utc)
        if stop_date.timestamp() > now_date.timestamp():
            profile_id = token_type.objects.filter(token=token).first().profile_id

            del user_data['token']
            return func(profile_id, user_data)
        else:
            raise AppError(
                {
                    'error_type': ErrorType.TOKEN_ERROR,
                    'description': 'the token is invalid, need to log in'
                }
            )
    return wrapper


class Access:
    """
    Get access to the application.
    """

    @staticmethod
    def register(user_data: Dict[str, str], profile_type: Type, email_token_type: Type) -> None:
        """
        Registration of a new user in the system.
        :param user_data: dict containing keys - email, password, (name, surname,)
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
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
        data_token = Access.create_token(profile_type.objects.create(**user_data))
        email_token_type.objects.create(**data_token)

        token = data_token['token']
        Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')

    @staticmethod
    def repeat_notification(user_data: Dict[str, str], profile_type: Type, email_token_type: Type) -> None:
        """
        Resend the email to the specified address.
        :param user_data: dict containing key - email
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :return: None
        :raises AppError: if the user is not registered in the system
        :raises AppError: if the user has already confirmed their profile
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
    def confirm_email(token: str, profile_type: Type, email_token_type: Type) -> None:
        """
        Confirms the user's profile.
        :param token: string with token
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :return: None
        :raises AppError: if email token is invalid
        :raises AppError: if email token does not exist
        """
        obj = email_token_type.objects.filter(token=token).first().profile_id
        if obj:
            stop_date = email_token_type.objects.filter(token=token).first().stop_date
            now_date = datetime.datetime.now(datetime.timezone.utc)
            if obj and stop_date.timestamp() > now_date.timestamp():
                profile_type.objects.filter(id=obj).update(active_account=True)
                email_token_type.objects.filter(token=token).first().delete()
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.EMAIL_TOKEN_ERROR,
                        'description': 'Email token is invalid'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.EMAIL_TOKEN_ERROR,
                    'description': 'Email token does not exist'
                }
            )

    @staticmethod
    def login(user_data: Dict[str, str], profile_type: Type, token_type: Type) -> str:
        """
        User authorization in the system.
        :param user_data: dict containing keys - email, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: object - TokenBuyer or TokenSeller
        :return: application access token
        :raises AppError: if the user entered an incorrect email or password
        :raises AppError: if the user is not registered.
        """
        email = Email.objects.filter(email=user_data['email']).first()
        if email:
            user = profile_type.objects.filter(email=email).first()
            if user.active_account:
                password_hash = Access.create_hash(user_data['password'])
                if user.password == password_hash:
                    data_token = Access.create_token(user)
                    token_type.objects.create(**data_token)
                    return data_token['token']
                else:
                    raise AppError(
                        {
                            'error_type': ErrorType.ACCESS_ERROR,
                            'description': 'invalid email or password'
                        }
                    )
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
    def reset_password(user_data: Dict[str, str], profile_type: Type, token_type: Type) -> None:
        """
        Changing the password to a new one
        :param user_data: dict containing keys - email, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: object - TokenBuyer or TokenSeller
        :return: None
        :raises AppError: if user is not registered
        """
        email = Email.objects.filter(email=user_data['email']).first()
        if email:
            profile = profile_type.objects.filter(email=email).first()
            if profile:
                token_type.objects.filter(profile=profile).delete()
                hash_password = Access.create_hash(user_data['password'])
                profile_type.objects.filter(email=email).update(password=hash_password)
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
    def logout(user_data: Dict[str, str], token_type: Type) -> None:
        """
        Authorized user logs out of the system.
        :param user_data: dict containing key - token
        :param token_type: object - TokenBuyer or TokenSeller
        :return: None
        :raises AppError: if token does not exist
        """
        if token_type.objects.filter(token=user_data['token']).first():
            token_type.objects.filter(token=user_data['token']).delete()
        else:
            raise AppError(
                {
                    'error_type': ErrorType.TOKEN_ERROR,
                    'description': 'Token does not exist'
                }
            )

    @staticmethod
    def update_profile(
            profile_id: Union[TokenBuyer, TokenSeller],
            user_data: Dict[str, str],
            profile_type: Type,
            token_type: Type
    ) -> Optional[str]:
        """
        Authorized user changes his profile data.
        :param profile_id: instance of object TokenBuyer or TokenSeller
        :param user_data: dict containing keys - name, surname, password
        :param profile_type: object - ProfileBuyer or ProfileSeller
        :param token_type: object - TokenBuyer or TokenSeller
        :return: new token or None
        """
        if 'password' not in user_data:
            profile_type.objects.filter(id=profile_id).update(**user_data)
        else:
            user_data['password'] = Access.create_hash(user_data['password'])
            new_token = Access.create_token(profile_id)
            token_type.objects.filter(profile=profile_id).delete()
            token_type.objects.update(**new_token)

            profile_type.objects.filter(id=profile_id).update(**user_data, active_account=False)
            email = list(profile_type.objects.filter(id=profile_id).values('email'))[0]['email']
            email = list(Email.objects.filter(id=email).values('email'))[0]['email']

            Access.send_notification([email], f'')
            return new_token['token']
        return None

    @staticmethod
    def create_token(profile_id: Union[TokenBuyer, TokenSeller]) -> dict:
        """
        JWT token generation
        :param profile_id: instance of object TokenBuyer or TokenSeller
        :return: dict with a token and its expiration date
        :return: example {"profile": obj, "token": "12345", "stop_date": 2023-12-27 10:37:08.84}
        """
        stop_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        payload = {"sub": "admin",
                   "exp": stop_date
                   }
        return {'profile': profile_id,
                'token': jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256"),
                'stop_date': stop_date
                }

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
