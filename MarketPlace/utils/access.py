import datetime

import hashlib
import json
import smtplib
import jwt

from django.http import HttpResponse, JsonResponse

from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD
from buyer.models import Email, TokenBuyer
from seller.models import TokenSeller


def decorator_authentication(func):
    """
    Token validation.
    """

    def wrapper(*args):
        request = args[0]
        body = json.loads(request.body)
        token = body['token']
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
        del body['token']
        return func(profile, body)

    return wrapper


class Access:
    """
    Get access to the application.
    """

    @staticmethod
    def register(user_data, profile_type, email_token_type) -> HttpResponse:
        """
        Registration of a new user in the system.
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :param profile_type: object - ProfileBuyer or  ProfileSeller
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
            user_data['email'] = Email.objects.create(email=user_email)

        user_data['password'] = Access.create_hash(user_data['password'])
        data_token = Access.create_token(profile_type.objects.create(**user_data))
        email_token_type.objects.create(**data_token)

        token = data_token['token']
        Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')
        return HttpResponse(status=201)

    @staticmethod
    def repeat_notification(user_data, profile_type, email_token_type) -> HttpResponse:
        """
        Resend the email to the specified address.
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :param profile_type: object - ProfileBuyer or  ProfileSeller
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
                profile = profile_type.objects.filter(email=email).first()
                data_token = Access.create_token(profile)
                email_token_type.objects.filter(profile=profile).update(**data_token)

                token = data_token['token']
                Access.send_notification([user_email], f'http://localhost/confirm/?token={token}')
            else:
                raise ValueError('The users email has been confirmed')
        else:
            raise ValueError('it is necessary to register')
        return HttpResponse(status=201)

    @staticmethod
    def confirm_email(token, profile_type, email_token_type) -> HttpResponse:
        """
        Confirms the user's profile.
        :param email_token_type: object - TokenEmailBuyer or TokenEmailSeller
        :param profile_type: object - ProfileBuyer or  ProfileSeller
        :param token: a dictionary containing key: token
        :return: "created" (201) response code
        :raises ValueError: if the token has expired
        """
        obj = email_token_type.objects.filter(token=token).first().profile_id
        stop_date = email_token_type.objects.filter(token=token).first().stop_date
        now_date = datetime.datetime.now()
        if obj and stop_date.timestamp() > now_date.timestamp():
            profile_type.objects.filter(id=obj).update(active_account=True)
            email_token_type.objects.filter(token=token).first().delete()
            return HttpResponse(status=201)
        else:
            raise ValueError('token is invalid')

    @staticmethod
    def login(user_data, profile_type, token_type) -> JsonResponse:
        """
        User authorization in the system.
        :param token_type: object - TokenBuyer or TokenSeller
        :param profile_type: object - ProfileBuyer or  ProfileSeller
        :param user_data: dictionary containing keys: email, password
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
                return JsonResponse(data_token['token'], status=200, safe=False)
            else:
                raise ValueError('invalid username or password')
        else:
            raise ValueError('user does not exist')

    @staticmethod
    def redirect_reset(user_data, profile_type) -> HttpResponse:
        """

        :param user_data: dictionary containing key with email
        :param profile_type:  object - ProfileBuyer or  ProfileSeller
        :return:
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

        return HttpResponse(status=201)

    @staticmethod
    def reset_password(user_data, profile_type, token_type) -> HttpResponse:
        """
        :param token_type: object - TokenBuyer or TokenSeller
        :param user_data: dictionary containing keys with email, password
        :param profile_type:  object - ProfileBuyer or  ProfileSeller
        :return:
        """
        email = Email.objects.filter(email=user_data['email']).first()
        profile = profile_type.objects.filter(email=email).first()
        token_type.objects.filter(profile=profile).delete()
        hash_password = Access.create_hash(user_data['password'])
        profile_type.objects.filter(email=email).update(password=hash_password)
        return HttpResponse(status=201)

    @staticmethod
    def logout(user_data, token_type) -> HttpResponse:
        """
        :param token_type: object - TokenBuyer or TokenSeller
        :param user_data: dictionary containing key with token
        :return:
        """
        token_type.objects.filter(token=user_data['token']).delete()
        return HttpResponse(status=201)

    @staticmethod
    def update_profile(profile, data, profile_type, token_type) -> HttpResponse:
        """
        :param token_type:
        :param profile_type:
        :param profile: object ProfileBuyer
        :param data: dictionary containing keys with
        :return:
        """
        if 'password' not in data:
            profile_type.objects.filter(id=profile.id).update(**data)
        else:
            data['password'] = Access.create_hash(data['password'])
            new_token = Access.create_token(profile)
            token_type.objects.filter(id=profile.id).delete()
            token_type.objects.update(**new_token)

            obj = profile_type.objects.filter(id=profile.id).update(**data, active_account=False)
            email = list(Email.objects.filter(id=obj).values('email'))[0]['email']

            Access.send_notification([email], f'xxx')

            return JsonResponse(new_token['token'], status=201, safe=False)

        return HttpResponse(status=201)

    @staticmethod
    def create_token(profile_type) -> dict:
        """
        JWT token generation
        :return: dict with a token and its expiration date, example {"token": "12345", "stop_date": 2023-12-27 10:37:08.84}
        """
        stop_date = datetime.datetime.now() + datetime.timedelta(hours=24)
        payload = {"sub": "admin", "exp": stop_date}
        return {'profile': profile_type,
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
