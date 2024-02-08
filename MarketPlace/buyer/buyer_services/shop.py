from django.http import JsonResponse, HttpResponse

from buyer.models import ProfileBuyer, ShoppingCart
from seller.models import CatalogProduct, Product


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

    @staticmethod
    def add_cart(profile, data) -> HttpResponse:
        """
        Authorized user adds the item to the shopping cart for further buying.
        :param profile: object ProfileBuyer
        :param data: dictionary containing keys with token, id product, quantity
        :return: "created" (201) response code
        """
        data['buyer'] = ProfileBuyer.objects.filter(id=profile.id).first()
        available_quantity = list(Product.objects.filter(id=data['product_id']).values('quantity'))[0]['quantity']
        if data['quantity'] <= available_quantity:
            ShoppingCart.objects.create(**data)
        else:
            raise ValueError(f'the available quantity of the product:{available_quantity}')
        return HttpResponse(status=201)

    @staticmethod
    def remove_cart(profile, data) -> HttpResponse:
        """
        Remove items from the shopping cart.
        :param profile: object ProfileBuyer
        :param data: dictionary containing keys with token, id product, quantity
        :return: "created" (201) response code
        """
        data['buyer'] = ProfileBuyer.objects.filter(id=profile.id).first()
        available_quantity = list(Product.objects.filter(id=data['product_id']).values('quantity'))[0]['quantity']
        if data['quantity'] <= available_quantity:
            if data['quantity'] == 0:
                ShoppingCart.objects.filter(buyer=data['buyer'], product_id=data["product_id"]).delete()
            else:
                ShoppingCart.objects.update_or_create(**data)
        else:
            raise ValueError(f'the available quantity of the product:{available_quantity}')
        return HttpResponse(status=201)