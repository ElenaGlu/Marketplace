import datetime
import json

from django.http import JsonResponse, HttpResponse

from buyer.models import TokenMain, ProfileBuyer, ShoppingCart
from seller.models import CatalogProduct, Product


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


class Shop:

    @staticmethod
    def shop_get_product_from_catalog(title_catalog):
        obj = list(CatalogProduct.objects.filter(
            catalog_id=title_catalog['title_catalog']).values('product_id')
                   )
        list_product = []
        for elem in range(len(obj)):
            product = list(Product.objects.filter(id=obj[elem]['product_id']).values('id', 'title_product', 'price'))
            list_product.extend(product)
        return JsonResponse(list_product, status=200, safe=False)

    @staticmethod
    def shop_get_detail_product(obj):
        detail_info_product = list(Product.objects.filter(id=obj['id']).values())
        return JsonResponse(detail_info_product, status=200, safe=False)

    @staticmethod
    def shop_add_in_shop_cart(user, request, data):
        profile = ProfileBuyer.objects.filter(email=user).first()
        product = Product.objects.filter(id=data['id_product']).first()
        quantity = list(Product.objects.filter(id=data['id_product']).values('quantity'))
        if data['quantity'] <= quantity[0]['quantity']:
            ShoppingCart.objects.create(
                buyer=profile,
                product=product,
                quantity=json.loads(request.body)['quantity'])
        return HttpResponse(status=201)
