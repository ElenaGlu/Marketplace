import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from seller.models import ProfileSeller, TokenSeller, TokenEmailSeller
from seller.seller_services.seller_product import SellerProduct
from utils.access import Access, decorator_authentication


def seller_register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing strings: email,
                                                    store_name,
                                                    Individual_Taxpayer_Number,
                                                    type_of_organization,
                                                    country_of_registration,
                                                    password
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.register(user_data, ProfileSeller, TokenEmailSeller)


def seller_repeat_notification(request: HttpRequest) -> HttpResponse:
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
        return obj_auth.repeat_notification(user_data, ProfileSeller, TokenEmailSeller)


def seller_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """
    token = request.GET.get('token')
    obj_auth = Access()
    return obj_auth.confirm_email(token, ProfileSeller, TokenEmailSeller)


def seller_login(request: HttpRequest) -> JsonResponse:
    """
    User authorization in the system.
    :param request: JSON object containing strings: email, password
    :return: application access token
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        obj_auth = Access()
        return obj_auth.login(user_data, ProfileSeller, TokenSeller)


@decorator_authentication
def seller_load_product(profile, data) -> HttpResponse:
    """
    Uploading product information.
    :param profile: ProfileSeller object
    :param data: dict containing keys with title_product, description, quantity, price, catalog_id
    :return: "created" (201) response code
    """
    obj_product = SellerProduct()
    return obj_product.load_product(profile, data)


@decorator_authentication
def seller_change_product(email, data) -> HttpResponse:
    """
    Change the data of an existing product
    :param email: Email object
    :param data: dict containing keys with title_product, description, quantity, price, catalog_id, product_id
    :return: "created" (201) response code
    """
    obj_product = SellerProduct()
    return obj_product.change_product(data)
