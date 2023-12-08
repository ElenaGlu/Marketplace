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
    email = ["user_1@mail.ru", "user_2@mail.ru"]
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
