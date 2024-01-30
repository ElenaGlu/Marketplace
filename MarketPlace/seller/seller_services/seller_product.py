from django.http import HttpResponse

from seller.models import ProfileSeller, Product, CatalogProduct


class SellerProduct:
    @staticmethod
    def load_product(email, data) -> HttpResponse:
        """
        Uploading product information.
        :param email:
        :param data: dict containing keys: token, store_name_id, title_catalog,
                                                        title_product, description,
                                                        quantity, price, catalog_product
        :return: "created" (201) response code
        """
        # del data['token']
        seller = ProfileSeller.objects.filter(email=email.id).first()
        new_product = Product.objects.create(store_name_id=data['store_name_id'],
                                             title_product=data['title_product'],
                                             description=data['description'],
                                             quantity=data['quantity'],
                                             price=data['price'],
                                             )

        bulk_list = list()
        for elem in data['catalog_product']:
            bulk_list.append(
                CatalogProduct(catalog=elem, product=new_product)
            )

        CatalogProduct.objects.bulk_create(bulk_list)

        return HttpResponse(status=201)
