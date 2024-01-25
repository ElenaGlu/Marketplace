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
        token = json.loads(request.body)['token']
        stop_date = TokenMain.objects.filter(token=token).first().stop_date
        now_date = datetime.datetime.now()
        if stop_date.timestamp() > now_date.timestamp():
            email = TokenMain.objects.filter(token=token).first().email
        else:
            raise ValueError('the token is invalid, need to log in')
        return func(email, request)
    return wrapper


class Shop:

    @staticmethod
    def selects_products_by_category(catalog) -> JsonResponse:
        """
        Selection of products included in a specific catalog.
        :param catalog: dictionary containing key with id catalog
        :return: products included in the catalog
        """
        products = list(CatalogProduct.objects.filter(catalog_id=catalog['catalog']).values())

        products_by_category = []
        for obj in products:
            products_by_category.extend(
                list(Product.objects.filter(id=obj['product_id']).values('id', 'title_product', 'price')
                     )
            )
        return JsonResponse(products_by_category, status=200, safe=False)

    @staticmethod
    def detail_product(product):
        """
        Detailed information about the product.
        :param product: dictionary containing key with id product
        :return: detailed information about the product
        """
        detail_info_product = list(Product.objects.filter(id=product['id']).values())
        return JsonResponse(detail_info_product, status=200, safe=False)

    # @staticmethod
    # def add_cart(email, data):
    #     """
    #     Authorized user adds the item to the shopping cart for further buying.
    #     :param data:
    #     :param email:
    #     :return: "created" (201) response code
    #     """
    #     profile = ProfileBuyer.objects.filter(id=email).first()
    #     product = Product.objects.filter(id=data['product_id']).first()
    #     quantity = list(Product.objects.filter(id=data['product_id']).values('quantity'))
    #     if data['quantity'] <= quantity[0]['quantity']:
    #         ShoppingCart.objects.create(
    #             buyer_id=profile,
    #             product_id=data['product_id'],
    #             quantity=data['quantity'])
    #     return HttpResponse(status=201)