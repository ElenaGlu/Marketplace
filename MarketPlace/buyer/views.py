import json

from django.http import HttpRequest, JsonResponse, HttpResponse

from buyer.models import Email
from buyer.models import ProfileBuyer
from seller.models import Product, CatalogProduct


def register(request: HttpRequest) -> HttpResponse:
    """
    Registration of a new user in the system
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
            user = Email.objects.create(email=user_email)
        ProfileBuyer.objects.create(email=user, name=user_data['name'],
                                    surname=user_data['surname'], password=user_data['password'])
        return HttpResponse(status=201)


# def login(request: HttpRequest) -> HttpResponse:
#     """
#     User authorization in the system.
#     :param request: JSON object containing strings: email, password.
#     :return: "OK" (200) response code
#     :raises ValueError: if the user entered an incorrect email or password
#     """
#     if request.method == "POST":
#         user_data = json.loads(request.body)
#         email = user_data['email']
#         password = user_data['password']
#
#         user = authenticate(request, email=email, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             return HttpResponse(status=200)
#         else:
#             raise ValueError('invalid username or password')


def get_product_from_catalog(request: HttpRequest) -> JsonResponse:
    """
    Getting items related to a specific catalog.
    :param request: JSON object containing string: title_catalog.
    :return: products included in the catalog
    """
    if request.method == "POST":
        obj = list(CatalogProduct.objects.filter(
            catalog_id=json.loads(request.body)['title_catalog']).values('product_id')
                        )
        product = list(Product.objects.filter(id=obj[0]['product_id']).values())
        return JsonResponse(product, status=200, safe=False)

