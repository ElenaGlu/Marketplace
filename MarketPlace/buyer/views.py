import hashlib

import jwt
import datetime

import json

from django.http import HttpRequest, JsonResponse, HttpResponse

from buyer.models import Email, ProfileBuyer, TokenEmail, ShoppingCart, TokenMain
from config import DJANGO_SECRET_KEY, KEY_SENDER, KEY_SENDER_PASSWORD
from seller.models import CatalogProduct, Product

import smtplib


def register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing strings: email, name, surname, password.
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        user_email = user_data['email']
        user = Email.objects.filter(email=user_email).first()
        if user:
            if ProfileBuyer.objects.filter(email=user_email).first():
                raise ValueError('the user is already registered')
        else:
            stop_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            payload = {"sub": "admin", "exp": stop_date}
            token = jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256")

            user = Email.objects.create(email=user_email)
            TokenEmail.objects.create(
                email=user,
                token=token,
                stop_date=stop_date)

            send_notification([user_email], f'http://localhost/confirm/?token={token}&email={user_email}')
            salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
            ProfileBuyer.objects.create(
                email=user,
                name=user_data['name'],
                surname=user_data['surname'],
                password=hashlib.pbkdf2_hmac('sha256', user_data['password'].encode('utf-8'), salt, 100000).hex()
            )
        return HttpResponse(status=201)


def send_notification(email, txt):
    """
    Sends an email to the specified address.
    """
    sender = KEY_SENDER
    sender_password = KEY_SENDER_PASSWORD
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, sender_password)

    for to_item in email:
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            sender, to_item, 'Тема сообщения')
        msg += txt
        mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()


def confirm(request):
    token = request.GET.get('token')
    # email = request.GET.get('email')
    user = Email.objects.filter(email=email).first()
    token_in_db = TokenEmail.objects.filter(email=user).first().token
    if token == token_in_db:
        ProfileBuyer.objects.filter(email=user).update(active_account=True)
        return HttpResponse(status=201)
    else:
        raise ValueError('it is necessary to issue a token')


def login(request: HttpRequest) -> HttpResponse:
    """
    User authorization in the system.
    :param request: JSON object containing strings: email, password.
    :return: "OK" (200) response code
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        user = Email.objects.filter(email=user_data['email']).first()
        if user:
            salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
            password_hash = hashlib.pbkdf2_hmac('sha256', user_data['password'].encode('utf-8'), salt, 100000).hex()

            if ProfileBuyer.objects.filter(email=user).first().password == password_hash:
                payload = {"sub": "admin", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
                token = jwt.encode(payload, DJANGO_SECRET_KEY, algorithm="HS256")
                TokenMain.objects.create(
                    email=user,
                    token_main=token
                )
                return JsonResponse(token, status=200, safe=False)
            else:
                raise ValueError('invalid username or password')


def get_product_from_catalog(request: HttpRequest) -> JsonResponse:
    """
    Getting items related to a specific catalog.
    :param request: JSON object containing string with id title_catalog.
    :return: products included in the catalog
    """
    if request.method == "POST":
        obj = list(CatalogProduct.objects.filter(
            catalog_id=json.loads(request.body)['title_catalog']).values('product_id')
                   )
        list_product = []
        for elem in range(len(obj)):
            product = list(Product.objects.filter(id=obj[elem]['product_id']).values('id', 'title_product', 'price'))
            list_product.extend(product)
        return JsonResponse(list_product, status=200, safe=False)


def get_detail_product(request: HttpRequest) -> JsonResponse:
    """
    Getting detailed information about the product.
    :param request: JSON object containing string with id product
    :return: detailed information about the product
    """
    if request.method == "POST":
        detail_info_product = list(Product.objects.filter(id=json.loads(request.body)['id']).values())
        return JsonResponse(detail_info_product, status=200, safe=False)


def add_in_shop_cart(request: HttpRequest) -> HttpResponse:
    """
    Adding an item to the shopping cart by an authorized user.
    :param request: JSON object containing string with id product, user's email and user's main token
    :return: "OK" (200) response code
    """
    if request.method == "POST":
        email = Email.objects.filter(email=json.loads(request.body)['user']).first()
        profile = ProfileBuyer.objects.filter(email=email).first()
        token = TokenMain.objects.filter(email=email).first().token_main
        if token == json.loads(request.body)['token_main']:
            product = Product.objects.filter(id=json.loads(request.body)['id']).first()
            ShoppingCart.objects.create(buyer=profile, product=product, quantity=json.loads(request.body)['quantity'])
        return HttpResponse(status=200)
