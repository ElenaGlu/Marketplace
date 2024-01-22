import datetime
import json

from django.http import HttpRequest, JsonResponse, HttpResponse


from buyer.models import ProfileBuyer, ShoppingCart, TokenMain
from seller.models import CatalogProduct, Product
from utils.Auth import Auth


def register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing strings: email, name, surname, password.
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Auth()
        return obj_auth.user_register(user_data)


def repeat_notification(request: HttpRequest) -> HttpResponse:
    """
    Resend the email to the specified address.
    :param request: JSON object containing string: email.
    :return: "created" (201) response code
    :raises ValueError: if the user is not registered in the system
    :raises ValueError: if the user has already confirmed their profile
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Auth()
        return obj_auth.user_repeat_notification(user_data)


def confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """
    token = request.GET.get('token')
    obj_auth = Auth()
    return obj_auth.user_confirm_email(token)


def login(request: HttpRequest) -> HttpResponse:
    """
    User authorization in the system.
    :param request: JSON object containing strings: email, password.
    :return: "OK" (200) response code
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Auth()
        return obj_auth.user_login(user_data)


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


def authentication_decorator(func):
    """
    Token validation.
    """

    def wrapper(*args):
        request = args[0]
        token_main = json.loads(request.body)['token_main']
        stop_date = TokenMain.objects.filter(token_main=token_main).first().stop_date
        now_date = datetime.datetime.now()
        if stop_date.timestamp() > now_date.timestamp():
            user = TokenMain.objects.filter(token_main=token_main).first().email
        else:
            raise ValueError('the token is invalid, need to log in')
        x = func(user, args[0])
        return x

    return wrapper


@authentication_decorator
def add_in_shop_cart(user, *args) -> HttpResponse:
    """
    Adding an item to the shopping cart by an authorized user.
    :param user: user's id
    :param args: JSON object containing string with product's id
    :return: "created" (201) response code
    """
    request = args[0]
    data = json.loads(request.body)
    profile = ProfileBuyer.objects.filter(email=user).first()
    product = Product.objects.filter(id=data['id_product']).first()
    quantity = list(Product.objects.filter(id=data['id_product']).values('quantity'))
    if data['quantity'] <= quantity[0]['quantity']:
        ShoppingCart.objects.create(
            buyer=profile,
            product=product,
            quantity=json.loads(request.body)['quantity'])
    return HttpResponse(status=201)
