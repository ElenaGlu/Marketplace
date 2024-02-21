from buyer.models import ProfileBuyer, ShoppingCart
from seller.models import CatalogProduct, Product


class Shop:

    @staticmethod
    def selects_products_by_category(catalog) -> list:
        """
        Selection of products included in a specific catalog.
        :param catalog: dict containing key - catalog
        :return: products (id, price, title_product) included in the catalog
        """
        products = list(CatalogProduct.objects.filter(catalog_id=catalog['catalog']).values())

        products_by_category = []
        for obj in products:
            products_by_category.extend(
                list(Product.objects.filter(id=obj['product_id']).values('id', 'title_product', 'price')
                     )
            )
        return products_by_category

    @staticmethod
    def detail_product(product) -> list:
        """
        Detailed information about the product.
        :param product: dictionary containing key - id
        :return: detailed information about the product (id, description, price, quantity, store_name_id, title_product)
        """
        return list(Product.objects.filter(id=product['id']).values())

    @staticmethod
    def add_cart(profile, data) -> None:
        """
        Authorized user adds the item to the shopping cart for further buying.
        :param profile: object ProfileBuyer
        :param data: dict containing keys - product_id, quantity
        :return: None
        :raises ValueError: if the requested quantity of goods is not available
        """
        data['buyer'] = ProfileBuyer.objects.filter(id=profile.id).first()
        available_quantity = list(Product.objects.filter(id=data['product_id']).values('quantity'))[0]['quantity']
        if data['quantity'] <= available_quantity:
            ShoppingCart.objects.create(**data)
        else:
            raise ValueError(f'the available quantity of the product:{available_quantity}')

    @staticmethod
    def change_cart(profile, data) -> None:
        """
        Authorized user changes the quantity of the product in the cart.
        :param profile: object ProfileBuyer
        :param data: dict containing keys - product_id, quantity
        :return: None
        :raises ValueError: if the requested quantity of goods is not available
        """
        data['buyer'] = ProfileBuyer.objects.filter(id=profile.id).first()
        order = data['quantity']
        available_quantity = list(Product.objects.filter(id=data['product_id']).values('quantity'))[0]['quantity']
        if order <= available_quantity:
            ShoppingCart.objects.update_or_create(**data)
        else:
            raise ValueError(f'You cannot add {order} products. Available for adding {available_quantity}')

    @staticmethod
    def remove_cart(profile, data) -> None:
        """
        Authorized user removes an item from the shopping cart.
        :param profile: object ProfileBuyer
        :param data: dict containing key - product_id
        :return: None
        """
        buyer = ProfileBuyer.objects.filter(id=profile.id).first()
        ShoppingCart.objects.filter(buyer=buyer, product_id=data["product_id"]).delete()

