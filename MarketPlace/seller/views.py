import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from seller.models import ProfileSeller, TokenEmailSeller, TokenSeller
from seller.seller_services.section_product import SectionProduct
from utils.access import Access, authentication_check


def seller_register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system.
    :param request: JSON object containing keys - email,
                                                  store_name,
                                                  individual_taxpayer_number,
                                                  type_of_organization,
                                                  country_of_registration,
                                                  password
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.register(json.loads(request.body), ProfileSeller, TokenEmailSeller)
        return HttpResponse(status=201)


def seller_repeat_notification(request: HttpRequest) -> HttpResponse:
    """
    Resend the email to the specified address.
    :param request: JSON object containing key - email
    :return: "created" (201) response code
    :raises ValueError: if the user is not registered in the system
    :raises ValueError: if the user has already confirmed their profile
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.repeat_notification(json.loads(request.body), ProfileSeller, TokenEmailSeller)
        return HttpResponse(status=201)


def seller_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """
    obj_auth = Access()
    obj_auth.confirm_email(request.GET.get('token'), ProfileSeller, TokenEmailSeller)
    return HttpResponse(status=201)


def seller_login(request: HttpRequest) -> JsonResponse:
    """
    User authorization in the system.
    :param request: JSON object containing keys - email, password
    :return: application access token
    :raises ValueError: if the user entered an incorrect email or password
    """
    if request.method == "POST":
        obj_auth = Access()
        token = obj_auth.login(json.loads(request.body), ProfileSeller, TokenSeller)
        return JsonResponse(token, status=200, safe=False)


def seller_redirect_reset(request: HttpRequest) -> HttpResponse:
    """
    Sends a link to the email to reset the password.
    :param request: JSON object containing key - email
    :return: "created" (201) response code
    :raises ValueError: if the user entered an incorrect email
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.redirect_reset(json.loads(request.body), ProfileSeller)
        return HttpResponse(status=201)


def seller_reset_password(request: HttpRequest) -> HttpResponse:
    """
    Changing the password to a new one.
    :param request: JSON object containing keys - email, new password
    :return: "created" (201) response code
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.reset_password(json.loads(request.body), ProfileSeller, TokenSeller)
        return HttpResponse(status=201)


def seller_logout(request: HttpRequest) -> HttpResponse:
    """
    Authorized user logs out of the system.
    :param request: JSON object containing key - token
    :return: "OK" (200) response code
    """
    if request.method == "POST":
        obj_auth = Access()
        obj_auth.logout(json.loads(request.body), TokenSeller)
        return HttpResponse(status=200)


@authentication_check
def seller_update_profile(profile, user_data) -> HttpResponse:
    """
    Authorized user changes his profile data.
    :param profile: object ProfileSeller
    :param user_data: dict containing keys - store_name, individual_taxpayer_number, type_of_organization,
    :return: "created" (201) response code
    """
    obj_auth = Access()
    return obj_auth.update_profile(profile, user_data, ProfileSeller, TokenSeller)


@authentication_check
def seller_load_product(profile, data) -> HttpResponse:
    """
    Uploading product information.
    :param profile: ProfileSeller object
    :param data: dict containing keys with title_product, description, quantity, price, catalog_id
    :return: "created" (201) response code
    """
    obj_product = SectionProduct()
    obj_product.load_product(profile, data)
    return HttpResponse(status=201)


@authentication_check
def seller_change_product(email, data) -> HttpResponse:
    """
    Change the data of an existing product
    :param email: Email object
    :param data: dict containing keys - title_product, description, quantity, price, catalog_id, product_id
    :return: "created" (201) response code
    """
    obj_product = SectionProduct()
    obj_product.change_product(data)
    return HttpResponse(status=201)


@authentication_check
def seller_archive_product(email, data) -> HttpResponse:
    """
    Adding an item to the archive.
    :param email: Email object
    :param data: dict containing keys - token, product_id
    :return: "created" (201) response code
    """
    obj_product = SectionProduct()
    obj_product.archive_product(data)
    return HttpResponse(status=201)
