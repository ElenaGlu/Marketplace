import json

from django.http import HttpRequest, JsonResponse, HttpResponse

from buyer.models import ProfileBuyer, TokenBuyer, TokenEmailBuyer
from seller.models import Catalog
from utils.access import Access, decorator_authentication
from buyer.buyer_services.shop import Shop


def buyer_register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing strings with email, name, surname, password
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.register(user_data, ProfileBuyer, TokenEmailBuyer)


def buyer_repeat_notification(request: HttpRequest) -> HttpResponse:
    """
    Resend the email to the specified address.
    :param request: JSON object containing string with email
    :return: "created" (201) response code
    :raises ValueError: if the user is not registered in the system
    :raises ValueError: if the user has already confirmed their profile
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.repeat_notification(user_data, ProfileBuyer, TokenEmailBuyer)


def buyer_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """

    token = request.GET.get('token')
    obj_auth = Access()
    return obj_auth.confirm_email(token, ProfileBuyer, TokenEmailBuyer)


def buyer_login(request: HttpRequest) -> JsonResponse:
    """
    User authorization in the system.
    :param request: JSON object containing strings with email, password
    :return: application access token
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.login(user_data, ProfileBuyer, TokenBuyer)


def buyer_redirect_reset(request: HttpRequest) -> HttpResponse:
    """
    Sends a link to the email to reset the password
    :param request: JSON object containing string with email
    :return: "created" (201) response code
    :raises ValueError: if the user entered an incorrect email
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.redirect_reset(user_data, ProfileBuyer)


def buyer_reset_password(request: HttpRequest) -> HttpResponse:
    """
    Changing the password to a new one
    :param request: JSON object containing strings with email, password
    :return: "created" (201) response code
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.reset_password(user_data, ProfileBuyer, TokenBuyer)


def buyer_logout(request: HttpRequest) -> HttpResponse:
    """
    Authorized user logs out of the system.
    :param request: JSON object containing string with token
    :return: "OK" (200) response code
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.logout(user_data, TokenBuyer)


@decorator_authentication
def buyer_update_profile(profile, user_data) -> HttpResponse:
    """
    Authorized user changes his profile data.
    :param profile: object ProfileBuyer
    :param user_data: dict containing keys with name, surname, password
    :return: "created" (201) response code
    """
    obj_auth = Access()
    return obj_auth.update_profile(profile, user_data, ProfileBuyer, TokenBuyer)


def buyer_provide_catalogs(request: HttpRequest) -> JsonResponse:
    """
    Provides a list id of existing catalogs.
    :return: id catalogs
    """
    if request.method == "GET":
        catalogs = list(Catalog.objects.all().values())
        return JsonResponse(catalogs, status=200, safe=False)


def buyer_selects_products_by_category(request: HttpRequest) -> JsonResponse:
    """
    Selection of products included in a specific catalog.
    :param request: JSON object containing string with id catalog
    :return: products included in the catalog
    """
    if request.method == "POST":
        catalog = json.loads(request.body)
        obj_shop = Shop()
        return obj_shop.selects_products_by_category(catalog)


def buyer_detail_product(request: HttpRequest) -> JsonResponse:
    """
    Detailed information about the product.
    :param request: JSON object containing string with id product
    :return: detailed information about the product
    """
    if request.method == "POST":
        obj = json.loads(request.body)
        obj_shop = Shop()
        return obj_shop.detail_product(obj)


@decorator_authentication
def buyer_add_cart(profile, data) -> HttpResponse:
    """
    Authorized user adds the item to the shopping cart for further buying.
    :param profile: object ProfileBuyer
    :param data: dict containing keys with token, id product, quantity
    :return: "created" (201) response code
    """
    obj_shop = Shop()
    return obj_shop.add_cart(profile, data)


@decorator_authentication
def buyer_remove_cart(profile, data) -> HttpResponse:
    """
    Remove items from the shopping cart.
    :param profile: object ProfileBuyer
    :param data: dict containing keys
    :return: "created" (201) response code
    """
    obj_shop = Shop()
    return obj_shop.remove_cart(profile, data)
