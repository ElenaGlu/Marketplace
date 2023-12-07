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
def fixture_email():
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
    tmp_list = []
    for item in email:
        tmp_list.append(models.Email(email=item['fields']['email']))
    models.Email.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_profile_seller(fixture_email):
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
    tmp_list = []
    for item in profile_seller:
        tmp_list.append(models.ProfileSeller(store_name=item['fields']['store_name'],
                                             Individual_Taxpayer_Number=item['fields']['Individual_Taxpayer_Number'],
                                             type_of_organization=item['fields']['type_of_organization'],
                                             country_of_registration=item['fields']['country_of_registration'],
                                             password=item['fields']['password'],
                                             email_id=item['fields']['email']
                                             )
                        )
    models.ProfileSeller.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_catalog():
    catalog = [
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
    tmp_list = []
    for item in catalog:
        tmp_list.append(models.Catalog(title_catalog=item['fields']['title_catalog']))
    models.Catalog.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_product(fixture_catalog):
    product = [
        {
            "model": "seller.product",
            "pk": 1,
            "fields": {
                "store_name": "1",
                "title_product": "product_1",
                "description": "description_1",
                "quantity": 1,
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
                "quantity": 2,
                "price": 2,
                "catalogs": "furniture"
            }
        }
    ]
    tmp_list = []
    for item in product:
        tmp_list.append(models.Product(store_name_id=item['fields']['store_name'],
                                       title_product=item['fields']['title_product'],
                                       description=item['fields']['description'],
                                       quantity=item['fields']['quantity'],
                                       price=item['fields']['price']
                                       )
                        )
    models.Product.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_catalog_product(fixture_product):
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
    tmp_list = []
    for item in catalog_product:
        tmp_list.append(models.CatalogProduct(product_id=item['fields']['product'],
                                              catalog_id=item['fields']['catalog']))
    models.CatalogProduct.objects.bulk_create(tmp_list)


@pytest.mark.django_db
def test_get_product_from_catalog(client, fixture_profile_seller, fixture_catalog_product):
    url = reverse('get_product_from_catalog')
    data = json.dumps({"title_catalog": 1})

    response = client.post(url, data, content_type='application/json')
    res = response.json()
    assert res == [{'id': 1,
                    'store_name_id': 1,
                    'title_product': 'product_1',
                    'description': 'description_1',
                    'quantity': 1,
                    'price': '1.00'}]
