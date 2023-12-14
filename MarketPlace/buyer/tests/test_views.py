import hashlib
import json
import os

import pytest
from django.urls import reverse

from seller import models
from buyer import models


@pytest.fixture()
def fixture_email():
    email = ["seller_1@mail.ru", "seller_2@mail.ru", "buyer_1@mail.ru"]
    tmp_list = []
    for item in email:
        tmp_list.append(models.Email(email=item))
    return models.Email.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_profile_seller(fixture_email):
    profile_seller = [
        {
            "store_name": "shop1",
            "Individual_Taxpayer_Number": "12345",
            "type_of_organization": "ИП",
            "country_of_registration": "RU",
            "password": "1",
            "email_id": fixture_email[0].id
        },
        {
            "store_name": "shop2",
            "Individual_Taxpayer_Number": "12345",
            "type_of_organization": "ИП",
            "country_of_registration": "RU",
            "password": "2",
            "email_id": fixture_email[1].id
        }
    ]
    tmp_list = []
    for item in profile_seller:
        tmp_list.append(models.ProfileSeller(store_name=item['store_name'],
                                             Individual_Taxpayer_Number=item['Individual_Taxpayer_Number'],
                                             type_of_organization=item['type_of_organization'],
                                             country_of_registration=item['country_of_registration'],
                                             password=item['password'],
                                             email_id=item['email_id']
                                             )
                        )
    return models.ProfileSeller.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_catalog():
    catalog = ["home", "furniture"]
    tmp_list = []
    for item in catalog:
        tmp_list.append(models.Catalog(title_catalog=item))
    return models.Catalog.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_product(fixture_catalog, fixture_profile_seller):
    product = [
        {
            "store_name": fixture_profile_seller[0].id,
            "title_product": "computer table",
            "description": "size:1500",
            "quantity": 10,
            "price": 1999,
        },
        {
            "store_name": fixture_profile_seller[1].id,
            "title_product": "flower",
            "description": "ficus",
            "quantity": 5,
            "price": 799,
        }
    ]
    tmp_list = []
    for item in product:
        tmp_list.append(models.Product(store_name_id=item['store_name'],
                                       title_product=item['title_product'],
                                       description=item['description'],
                                       quantity=item['quantity'],
                                       price=item['price']
                                       )
                        )
    return models.Product.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_catalog_product(fixture_product, fixture_catalog):
    catalog_product = [{"product": fixture_product[0].id, "catalog": fixture_catalog[0].id},
                       {"product": fixture_product[0].id, "catalog": fixture_catalog[1].id},
                       {"product": fixture_product[1].id, "catalog": fixture_catalog[0].id}
                       ]
    tmp_list = []
    for item in catalog_product:
        tmp_list.append(models.CatalogProduct(product_id=item['product'],
                                              catalog_id=item['catalog']))
    models.CatalogProduct.objects.bulk_create(tmp_list)


@pytest.fixture()
def fixture_profile_buyer(fixture_email):
    # salt = os.urandom(32)
    salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
    key = hashlib.pbkdf2_hmac('sha256', '1'.encode('utf-8'), salt, 100000).hex()
    profile_buyer = [
        {
            "name": "Ivan",
            "surname": "Ivanovich",
            "password": key,
            "email_id": fixture_email[2].id
        }
    ]
    tmp_list = []
    for item in profile_buyer:
        tmp_list.append(models.ProfileBuyer(name=item['name'], surname=item['surname'],
                                            password=item['password'], email_id=item['email_id']
                                            )
                        )
    return models.ProfileBuyer.objects.bulk_create(tmp_list)


@pytest.mark.django_db
def test_view_register(client, fixture_profile_buyer):
    url = reverse('register')
    data = json.dumps({'email': 'john@mail.ru', 'name': 'john',
                       'surname': 'piter', 'password': '123'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201

    # with pytest.raises(ValueError):
    #     data = json.dumps({'email': 'buyer_1@mail.ru', 'name': 'john',
    #                        'surname': 'piter', 'password': '123'})
    #     client.post(url, data, content_type='application/json')


@pytest.mark.django_db
def test_view_login(client, fixture_profile_buyer):
    url = reverse('login')
    data = json.dumps({'email': 'buyer_1@mail.ru', 'password': '1'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200

    # with pytest.raises(ValueError):
    #     data = json.dumps({'email': 'aa@mail.ru', 'password': '123'})
    #     client.post(url, data, content_type='application/json')


@pytest.mark.django_db
def test_get_product_from_catalog(client, fixture_profile_seller, fixture_catalog_product):
    url = reverse('get_product_from_catalog')
    data = json.dumps({"title_catalog": 1})

    response = client.post(url, data, content_type='application/json')
    res = response.json()
    assert res == [
        {'id': 1, 'price': '1999.00', 'title_product': 'computer table'},
        {'id': 2, 'price': '799.00', 'title_product': 'flower'}
    ]


@pytest.mark.django_db
def test_get_detail_product(client, fixture_profile_seller, fixture_catalog_product):
    url = reverse('get_detail_product')
    data = json.dumps({"id": 1})

    response = client.post(url, data, content_type='application/json')
    res = response.json()
    assert res == [{'description': 'size:1500',
                    'id': 1,
                    'price': '1999.00',
                    'quantity': 10,
                    'store_name_id': 1,
                    'title_product': 'computer table'}]

# @pytest.mark.django_db
# def test_add_in_shop_cart(client, fixture_profile_seller, fixture_catalog_product, fixture_profile_buyer):
#     url = reverse('add_in_shop_cart')
#     data = json.dumps({"id": 1, "user": 1})
#     response = client.post(url, data, content_type='application/json')
#
#     assert response.status_code == 201
