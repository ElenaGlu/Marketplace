import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from seller.models import Product, CatalogProduct, ProfileSeller
from utils.access import Access


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
        return obj_auth.user_register(user_data, ProfileSeller)


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
        return obj_auth.user_repeat_notification(user_data, ProfileSeller)


def seller_confirm_email(request) -> HttpResponse:
    """
    Confirms the user's profile.
    :param request: url with token
    :return: "created" (201) response code
    :raises ValueError: if the token has expired
    """
    token = request.GET.get('token')
    obj_auth = Access()
    return obj_auth.user_confirm_email(token, ProfileSeller)


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
        return obj_auth.user_login(user_data, ProfileSeller)


def load_product(request: HttpRequest) -> HttpResponse:
    """
    Uploading product information.
    :param request: JSON object containing strings: title_catalog, title_product, description, quantity, price
    :return: "created" (201) response code
    """
    if request.method == "POST":
        product_data = json.loads(request.body)
        new_product = Product.objects.create(title_product=product_data['title_product'],
                                             description=product_data['description'],
                                             quantity=product_data['quantity'],
                                             price=product_data['price']
                                             )
        for item in product_data['title_catalog']:
            product_item = CatalogProduct(product=new_product, catalog=item)

        return HttpResponse(status=201)
