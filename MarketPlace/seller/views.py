import json

from django.http import HttpRequest, HttpResponse

from seller.models import Product, CatalogProduct


def load_product(request: HttpRequest) -> HttpResponse:
    """
    Uploading product information.
    :param request: JSON object containing strings: title_catalog, title_product, description, quantity, price.
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
