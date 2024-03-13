import json
from typing import Dict

from django.http import HttpRequest, HttpResponse, JsonResponse

from buyer.buyer_services.shop import Shop
from buyer.models import ProfileBuyer, TokenBuyer
from seller.models import Catalog
from utils.access import Access, authentication_check


def buyer_register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing keys - email, name, surname, password
    :return: "created" (201) response code
    :raises AppError: if the user is registered in the system
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.register(json.loads(request.body), ProfileBuyer, 'TokenEmailBuyer')
        return HttpResponse(status=201)


def buyer_repeat_notification(request: HttpRequest) -> HttpResponse:
    """
    Resend the email to the specified address.
    :param request: JSON object containing key - email
    :return: "created" (201) response code
    :raises AppError: if the user is not registered in the system
    :raises AppError: if the user has already confirmed their profile
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.repeat_notification(json.loads(request.body), ProfileBuyer, 'TokenEmailBuyer')
        return HttpResponse(status=201)


def buyer_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises AppError: if email token is invalid
    :raises AppError: if email token does not exist
    """
    obj_auth = Access()
    obj_auth.confirm_email(request.GET.get('token'), ProfileBuyer, 'TokenEmailBuyer')
    return HttpResponse(status=201)


def buyer_login(request: HttpRequest) -> JsonResponse:
    """
    User authorization in the system.
    :param request: JSON object containing keys - email, password
    :return: application access token
    :raises AppError: if the user entered an incorrect email or password
    :raises AppError: if the user is not registered
    """
    if request.method == "POST":
        obj_auth = Access()
        token = obj_auth.login(json.loads(request.body), ProfileBuyer, 'TokenBuyer')
        return JsonResponse(token, status=200, safe=False)


def buyer_redirect_reset(request: HttpRequest) -> HttpResponse:
    """
    Sends a link to the email to reset the password.
    :param request: JSON object containing key - email
    :return: "created" (201) response code
    :raises AppError: if user is not registered
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.redirect_reset(json.loads(request.body), ProfileBuyer)
        return HttpResponse(status=201)


def buyer_reset_password(request: HttpRequest) -> HttpResponse:
    """
    Changing the password to a new one.
    :param request: JSON object containing keys - email,  new password
    :return: "created" (201) response code
    :raises AppError: if user is not registered
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.reset_password(json.loads(request.body), ProfileBuyer, TokenBuyer)
        return HttpResponse(status=201)


def buyer_logout(request: HttpRequest) -> HttpResponse:
    """
    Authorized user logs out of the system.
    :param request: JSON object containing key - token
    :return: "OK" (200) response code
    :raises AppError: if token does not exist
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.logout(json.loads(request.body), TokenBuyer)
        return HttpResponse(status=200)


@authentication_check(TokenBuyer)
def buyer_update_profile(profile_id: TokenBuyer, user_data: Dict[str, str]) -> HttpResponse:
    """
    Authorized user changes his profile data.
    :param profile_id: instance of object TokenBuyer
    :param user_data: dict containing keys - name, surname, password
    :return: "created" (201) response code
    """
    obj_auth = Access()
    new_token = obj_auth.update_profile(profile_id, user_data, ProfileBuyer, TokenBuyer)
    return JsonResponse(new_token, status=201, safe=False)


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
    :raises AppError: if there is no catalog with this id
    """
    if request.method == "POST":
        obj_shop = Shop()
        products_by_category = obj_shop.selects_products_by_category(json.loads(request.body))
        return JsonResponse(products_by_category, status=200, safe=False)


def buyer_detail_product(request: HttpRequest) -> JsonResponse:
    """
    Detailed information about the product.
    :param request: JSON object containing key - product_id
    :return: detailed information about the product (id, description, price, quantity,
                                                     store_name_id, title_product, active_status)
    :raises AppError: if there is no product with this id
    """
    if request.method == "POST":
        obj_shop = Shop()
        detail_info_product = obj_shop.detail_product(json.loads(request.body))
        return JsonResponse(detail_info_product, status=200, safe=False)


@authentication_check(TokenBuyer)
def buyer_add_cart(profile_id: TokenBuyer, data: Dict[str, int]) -> HttpResponse:
    """
    Authorized user adds the item to the shopping cart for further buying.
    :param profile_id: instance of object TokenBuyer
    :param data: dict containing keys - product_id, quantity
    :return: "created" (201) response code
    :raises AppError: if the requested quantity of product is not available
    """
    obj_shop = Shop()
    obj_shop.add_cart(profile_id, data)
    return HttpResponse(status=201)


@authentication_check(TokenBuyer)
def buyer_change_cart(profile_id: TokenBuyer, data: Dict[str, int]) -> HttpResponse:
    """
    Authorized user changes the quantity of the product in the cart.
    :param profile_id: instance of object TokenBuyer
    :param data: dict containing keys - product_id, quantity
    :return: "created" (201) response code
    :raises AppError: if the requested quantity of product is not available
    """
    obj_shop = Shop()
    obj_shop.change_cart(profile_id, data)
    return HttpResponse(status=201)


@authentication_check(TokenBuyer)
def buyer_remove_cart(profile_id: TokenBuyer, data: Dict[str, int]) -> HttpResponse:
    """
    Authorized user removes an item from the shopping cart.
    :param profile_id: instance of object TokenBuyer
    :param data: dict containing keys - product_id, quantity
    :return: "OK" (200) response code
    :raises AppError: if there is no such product in the cart
    """
    obj_shop = Shop()
    obj_shop.remove_cart(profile_id, data)
    return HttpResponse(status=200)
