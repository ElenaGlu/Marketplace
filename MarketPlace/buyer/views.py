import json

from django.http import HttpRequest, JsonResponse, HttpResponse

from buyer.models import ProfileBuyer, TokenBuyer, TokenEmailBuyer
from seller.models import Catalog
from utils.access import Access, decorator_authentication
from buyer.buyer_services.shop import Shop


def buyer_register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing keys - email, name, surname, password
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        obj_auth = Access()
        return obj_auth.register(json.loads(request.body), ProfileBuyer, TokenEmailBuyer)


def buyer_repeat_notification(request: HttpRequest) -> HttpResponse:
    """
    Resend the email to the specified address.
    :param request: JSON object containing key - email
    :return: "created" (201) response code
    :raises ValueError: if the user is not registered in the system
    :raises ValueError: if the user has already confirmed their profile
    """
    if request.method == "POST":
        obj_auth = Access()
        return obj_auth.repeat_notification(json.loads(request.body), ProfileBuyer, TokenEmailBuyer)


def buyer_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """
    obj_auth = Access()
    return obj_auth.confirm_email(request.GET.get('token'), ProfileBuyer, TokenEmailBuyer)


def buyer_login(request: HttpRequest) -> JsonResponse:
    """
    User authorization in the system.
    :param request: JSON object containing keys - email, password
    :return: application access token
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        obj_auth = Access()
        return obj_auth.login(json.loads(request.body), ProfileBuyer, TokenBuyer)


def buyer_redirect_reset(request: HttpRequest) -> HttpResponse:
    """
    Sends a link to the email to reset the password.
    :param request: JSON object containing key - email
    :return: "created" (201) response code
    :raises ValueError: if the user entered an incorrect email
    """
    if request.method == "POST":
        obj_auth = Access()
        return obj_auth.redirect_reset(json.loads(request.body), ProfileBuyer)


def buyer_reset_password(request: HttpRequest) -> HttpResponse:
    """
    Changing the password to a new one.
    :param request: JSON object containing keys - email, password
    :return: "created" (201) response code
    """
    if request.method == "POST":
        obj_auth = Access()
        return obj_auth.reset_password(json.loads(request.body), ProfileBuyer, TokenBuyer)


def buyer_logout(request: HttpRequest) -> HttpResponse:
    """
    Authorized user logs out of the system.
    :param request: JSON object containing key - token
    :return: "OK" (200) response code
    """
    if request.method == "POST":
        obj_auth = Access()
        return obj_auth.logout(json.loads(request.body), TokenBuyer)


@decorator_authentication
def buyer_update_profile(profile, user_data) -> HttpResponse:
    """
    Authorized user changes his profile data.
    :param profile: object ProfileBuyer
    :param user_data: dict containing keys - name, surname, password
    :return: "created" (201) response code
    """
    obj_auth = Access()
    return obj_auth.update_profile(profile, user_data, ProfileBuyer, TokenBuyer)


def buyer_provide_catalogs(request: HttpRequest) -> JsonResponse:
    """
    Provides a list id's (and title_catalog) of existing catalogs.
    :return: id's and title of catalogs
    """
    if request.method == "GET":
        catalogs = list(Catalog.objects.all().values())
        return JsonResponse(catalogs, status=200, safe=False)


def buyer_selects_products_by_category(request: HttpRequest) -> JsonResponse:
    """
    Selection of products included in a specific catalog.
    :param request: JSON object containing key - catalog
    :return: products (id, price, title_product) included in the catalog
    """
    if request.method == "POST":
        obj_shop = Shop()
        return obj_shop.selects_products_by_category(json.loads(request.body))


def buyer_detail_product(request: HttpRequest) -> JsonResponse:
    """
    Detailed information about the product.
    :param request: JSON object containing key - id
    :return: detailed information about the product (id, description, price, quantity, store_name_id, title_product)
    """
    if request.method == "POST":
        obj_shop = Shop()
        return obj_shop.detail_product(json.loads(request.body))


@decorator_authentication
def buyer_add_cart(profile, data) -> HttpResponse:
    """
    Authorized user adds the item to the shopping cart for further buying.
    :param profile: object ProfileBuyer
    :param data: dict containing keys - token, product_id, quantity
    :return: "created" (201) response code
    :raises ValueError: if the requested quantity of goods is not available
    """
    obj_shop = Shop()
    return obj_shop.add_cart(profile, data)


@decorator_authentication
def buyer_remove_cart(profile, data) -> HttpResponse:
    """
    Authorized user remove items from the shopping cart.
    :param profile: object ProfileBuyer
    :param data: dict containing keys - token, product_id, quantity
    :return: "created" (201) response code
    :raises ValueError: if the requested quantity of goods is not available
    """
    obj_shop = Shop()
    return obj_shop.remove_cart(profile, data)
