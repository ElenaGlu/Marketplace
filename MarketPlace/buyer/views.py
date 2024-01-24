import json

from django.http import HttpRequest, JsonResponse, HttpResponse

from buyer.models import ProfileBuyer
from utils.access import Access
from buyer.shop import Shop, authentication_decorator


def buyer_register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing strings: email, name, surname, password
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.user_register(user_data, ProfileBuyer)


def buyer_repeat_notification(request: HttpRequest) -> HttpResponse:
    """
    Resend the email to the specified address.
    :param request: JSON object containing string: email
    :return: "created" (201) response code
    :raises ValueError: if the user is not registered in the system
    :raises ValueError: if the user has already confirmed their profile
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.user_repeat_notification(user_data, ProfileBuyer)


def buyer_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """
    token = request.GET.get('token')
    obj_auth = Access()
    return obj_auth.user_confirm_email(token, ProfileBuyer)


def buyer_login(request: HttpRequest) -> JsonResponse:
    """
    User authorization in the system.
    :param request: JSON object containing strings: email, password
    :return: application access token
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.user_login(user_data, ProfileBuyer)


def get_product_from_catalog(request: HttpRequest) -> JsonResponse:
    """
    Getting items related to a specific catalog.
    :param request: JSON object containing string with id title_catalog
    :return: products included in the catalog
    """
    if request.method == "POST":
        title_catalog = json.loads(request.body)
        obj_shop = Shop()
        return obj_shop.shop_get_product_from_catalog(title_catalog)


def get_detail_product(request: HttpRequest) -> JsonResponse:
    """
    Getting detailed information about the product.
    :param request: JSON object containing string with id product
    :return: detailed information about the product
    """
    if request.method == "POST":
        obj = json.loads(request.body)
        obj_shop = Shop()
        return obj_shop.shop_get_detail_product(obj)


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
    obj_shop = Shop()
    return obj_shop.shop_add_in_shop_cart(user, request, data)
