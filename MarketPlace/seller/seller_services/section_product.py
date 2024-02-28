from typing import Dict, Union

from seller.models import Catalog, CatalogProduct, Product, TokenSeller, ProfileSeller


class SectionProduct:
    @staticmethod
    def load_product(profile_id: TokenSeller, data: Dict[str, Union[str, int, list[int]]]) -> None:
        """
        Uploading product information.
        :param profile_id: instance of object TokenSeller
        :param data: dict containing keys - title_product, description, quantity, price, catalog_id
        :return: None
        """
        data['store_name_id'] = ProfileSeller.objects.filter(id=profile_id).first().id
        catalogs = data.pop('catalog_id')
        new_product = Product.objects.create(**data)
        bulk_list = list()
        for elem in catalogs:
            catalog = Catalog.objects.filter(id=elem).first()
            bulk_list.append(
                CatalogProduct(catalog_id=catalog.id, product_id=new_product.id)
            )
        CatalogProduct.objects.bulk_create(bulk_list)

    @staticmethod
    def change_product(data: Dict[str, Union[str, int, list[int]]]) -> None:
        """
        Change the data of an existing product
        :param data: dict containing keys - title_product, description, quantity, price, catalog_id, product_id
        :return: None
        """
        catalogs = data.pop('catalog_id')
        product = data.pop('product_id')
        Product.objects.filter(id=product).update(**data)
        CatalogProduct.objects.filter(product_id=product).delete()

        bulk_list = list()
        for elem in catalogs:
            catalog = Catalog.objects.filter(id=elem).first()
            bulk_list.append(
                CatalogProduct(catalog_id=catalog.id, product_id=product)
            )
        CatalogProduct.objects.bulk_create(bulk_list)

    @staticmethod
    def archive_product(data: Dict[str, Union[str, int]]) -> None:
        """
        Adding an item to the archive.
        :param data: dict containing keys - token, product_id
        :return: None
        """
        Product.objects.filter(id=data['product_id']).update(active_status=False)
