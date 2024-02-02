from django.http import HttpResponse

from seller.models import Product, CatalogProduct, Catalog


class SellerProduct:
    @staticmethod
    def load_product(profile, data) -> HttpResponse:
        """
        Uploading product information.
        :param profile: ProfileSeller object
        :param data: dict containing keys with title_product, description, quantity, price, catalog_id
        :return: "created" (201) response code
        """
        data['store_name_id'] = profile.id
        catalogs = data.pop('catalog_id')
        new_product = Product.objects.create(**data)
        bulk_list = list()
        for elem in catalogs:
            catalog = Catalog.objects.filter(id=elem).first()
            bulk_list.append(
                CatalogProduct(catalog_id=catalog.id, product_id=new_product.id)
            )
        CatalogProduct.objects.bulk_create(bulk_list)

        return HttpResponse(status=201)

    @staticmethod
    def change_product(data) -> HttpResponse:
        """
        Change the data of an existing product
        :param data: dict containing keys with title_product, description, quantity, price, catalog_id, product_id
        :return: "created" (201) response code
        """
        catalogs = data.pop('catalog_id')
        product = data.pop('product_id')
        product_update = Product.objects.filter(id=product).update(**data)
        CatalogProduct.objects.filter(product_id=product).delete()

        bulk_list = list()
        for elem in catalogs:
            catalog = Catalog.objects.filter(id=elem).first()
            bulk_list.append(
                CatalogProduct(catalog_id=catalog.id, product_id=product_update)
            )
        CatalogProduct.objects.bulk_create(bulk_list)
        return HttpResponse(status=201)

