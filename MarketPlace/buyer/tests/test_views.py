import json

import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_register(client, fixture_profile_buyer):
    url = reverse('buyer_register')
    data = json.dumps({
        'email': 'shishalovae@mail.ru',
        'name': 'user',
        'surname': 'test_user',
        'password': 'password'}
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_repeat_notification(client, fixture_profile_buyer, fixture_token_email):
    url = reverse('buyer_repeat_notification')
    data = json.dumps({'email': 'elena.g.2023@list.ru'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_confirm_email(client, fixture_token_email, fixture_profile_buyer):
    url = reverse('buyer_confirm_email')
    data = {"token": "123"}
    response = client.get(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login(client, fixture_profile_buyer):
    url = reverse('buyer_login')
    data = json.dumps({
        'email': 'elena.g.2023@list.ru',
        'password': '1'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_selects_products_by_category(client, fixture_profile_seller, fixture_catalog_product):
    url = reverse('buyer_selects_products_by_category')
    data = json.dumps({"catalog": 1})
    response = client.post(url, data, content_type='application/json').json()
    assert response == [
        {'id': 1, 'price': '1999.00', 'title_product': 'computer table'},
        {'id': 2, 'price': '799.00', 'title_product': 'flower'}
    ]


@pytest.mark.django_db
def test_detail_product(client, fixture_profile_seller, fixture_catalog_product):
    url = reverse('buyer_detail_product')
    data = json.dumps({"id": 1})
    response = client.post(url, data, content_type='application/json').json()
    assert response == [
        {'description': 'size:1500',
         'id': 1,
         'price': '1999.00',
         'quantity': 10,
         'store_name_id': 1,
         'title_product': 'computer table'}
    ]


@pytest.mark.django_db
def test_add_cart(client, fixture_profile_seller, fixture_catalog_product,
                  fixture_profile_buyer, fixture_token_main, fixture_shopping_cart):
    url = reverse('buyer_add_cart')
    data = json.dumps(
        {"token": "111",
         "product_id": 1,
         "quantity": 2
         }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
