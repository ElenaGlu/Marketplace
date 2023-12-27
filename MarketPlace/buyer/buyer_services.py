import datetime
import hashlib
import smtplib

import jwt

from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD


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