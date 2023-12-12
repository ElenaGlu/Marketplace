import json

from django.http import HttpRequest, JsonResponse, HttpResponse

from buyer.models import Email, ShoppingCart
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


# def add_in_shop_cart(request: HttpRequest) -> HttpResponse:
#     """
#     Adding an item to the shopping cart by an authorized user.
#     :param request: JSON object containing string with id product and
#     :return: "OK" (200) response code
#     """
#     if request.method == "POST":
#         # buyer =  # токен/ключ/сессия/авторизация/  id user and filter()
#         product = Product.objects.filter(id=json.loads(request.body)['id'])
#
#         ShoppingCart.objects.create(buyer=buyer, product=product)
#         return HttpResponse(status=200)



