import json

import pytest
from django.urls import reverse

from seller import models


@pytest.mark.django_db
def test_view_register(client):
    url = reverse('register')
    data = json.dumps({'email': 'john@mail.ru', 'name': 'john',
                       'surname': 'piter', 'password': '123'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201

    with pytest.raises(ValueError):
        client.post(url, data, content_type='application/json')


# @pytest.mark.django_db
# def test_view_login(client):
#
#     create(username='john', email='john@mail.ru', password='123')
#
#     url = reverse('login')
#     data = json.dumps({'email': 'john@mail.ru', 'password': '123'})
#     response = client.post(url, data, content_type='application/json')
#     assert response.status_code == 200
#
#     with pytest.raises(ValueError):
#         data = json.dumps({'email': 'aa@mail.ru', 'password': '123'})
#         client.post(url, data, content_type='application/json')

@pytest.fixture()
def complete_db():
    email = [{
        "model": "buyer.Email",
        "pk": 1,
        "fields": {
            "email": "store_1@mail.ru"
        }
    },
        {
            "model": "buyer.Email",
            "pk": 2,
            "fields": {
                "email": "store_2@mail.ru"
            }
        }
    ]
    lst = []
    for item in email:
        lst.append(models.Email(email=item['fields']['email']))
    models.Email.objects.bulk_create(lst)

    profile_seller = [
        {
            "model": "seller.ProfileSeller",
            "pk": 1,
            "fields": {
                "store_name": "store_1",
                "Individual_Taxpayer_Number": "12345",
                "type_of_organization": "ИП",
                "country_of_registration": "RU",
                "password": "1",
                "email": "1"
            }
        },
        {
            "model": "seller.ProfileSeller",
            "pk": 2,
            "fields": {
                "store_name": "store_2",
                "Individual_Taxpayer_Number": "12345",
                "type_of_organization": "ИП",
                "country_of_registration": "RU",
                "password": "2",
                "email": "2"
            }
        }
    ]
    lst_2 = []
    for item in profile_seller:
        lst_2.append(models.ProfileSeller(store_name=item['fields']['store_name'],
                                          Individual_Taxpayer_Number=item['fields']['Individual_Taxpayer_Number'],
                                          type_of_organization=item['fields']['type_of_organization'],
                                          country_of_registration=item['fields']['country_of_registration'],
                                          password=item['fields']['password'],
                                          email_id=item['fields']['email']
                                          )
                     )
    models.ProfileSeller.objects.bulk_create(lst_2)

    seller_catalog = [
        {
            "model": "seller.catalog",
            "pk": 1,
            "fields": {
                "title_catalog": "home"
            }
        },
        {
            "model": "seller.catalog",
            "pk": 2,
            "fields": {
                "title_catalog": "furniture"
            }
        }
    ]
    lst_4 = []
    for item in seller_catalog:
        lst_4.append(models.Catalog(title_catalog=item['fields']['title_catalog']))
    models.Catalog.objects.bulk_create(lst_4)

    seller_product = [
        {
            "model": "seller.product",
            "pk": 1,
            "fields": {
                "store_name": "1",
                "title_product": "product_1",
                "description": "description_1",
                "quantity": "quantity_1",
                "price": 1,
                "catalogs": "home"
            }
        },
        {
            "model": "seller.product",
            "pk": 2,
            "fields": {
                "store_name": "2",
                "title_product": "product_2",
                "description": "description_2",
                "quantity": "quantity_2",
                "price": 2,
                "catalogs": "furniture"
            }
        }
    ]
    lst_5 = []
    for item in seller_product:
        lst_5.append(models.Product(store_name_id=item['fields']['store_name'],
                                    title_product=item['fields']['title_product'],
                                    description=item['fields']['description'],
                                    quantity=item['fields']['quantity'],
                                    price=item['fields']['price']
                                    )
                     )
    models.Product.objects.bulk_create(lst_5)

    catalog_product = [{
        "model": "seller.CatalogProduct",
        "pk": 1,
        "fields": {
            "product": "1",
            "catalog": "1"
        }
    },
        {
            "model": "seller.CatalogProduct",
            "pk": 2,
            "fields": {
                "product": "2",
                "catalog": "2"
            }
        }
    ]
    lst_3 = []
    for item in catalog_product:
        lst_3.append(models.CatalogProduct(product_id=item['fields']['product'],
                                           catalog_id=item['fields']['catalog']))
    models.CatalogProduct.objects.bulk_create(lst_3)


@pytest.mark.django_db
def test_get_products_from_catalog(client, complete_db):
    url = reverse('get_products_from_catalog')
    data = json.dumps({"title_catalog": 1})

    response = client.post(url, data, content_type='application/json')
    res = response.json()
    assert res == [{'id': 1,
                    'store_name_id': 1,
                    'title_product': 'product_1',
                    'description': 'description_1',
                    'quantity': 'quantity_1',
                    'price': '1.00'}]
