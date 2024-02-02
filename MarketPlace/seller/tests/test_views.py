import json

import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_register(client, fixture_profile_seller):
    url = reverse('seller_register')
    data = json.dumps(
        {'email': 'shishalovae@mail.ru',
         'store_name': 'store',
         'Individual_Taxpayer_Number': '12345',
         'type_of_organization': 'ИП',
         'country_of_registration': 'RU',
         'password': 'password'}
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_repeat_notification(client, fixture_profile_seller, fixture_token_email_seller):
    url = reverse('seller_repeat_notification')
    data = json.dumps({'email': 'elena.g.2023@list.ru'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_confirm_email(client, fixture_profile_seller, fixture_token_email_seller):
    url = reverse('seller_confirm_email')
    data = {"token": "123"}
    response = client.get(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login(client, fixture_profile_seller):
    url = reverse('seller_login')
    data = json.dumps(
        {'email': 'elena.g.2023@list.ru',
         'password': '1'}
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_load_product(client, fixture_token_seller, fixture_catalog_product):
    url = reverse('seller_load_product')
    data = json.dumps(
        {'token': '333',  # "seller_1@mail.ru"
         'title_product': 'bed',
         'description': 'double bed',
         'quantity': 6,
         'price': 7000,
         'catalog_id': [1, 2],
         }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_change_product(client, fixture_token_seller, fixture_catalog_product):
    url = reverse('seller_change_product')
    data = json.dumps(
        {'token': '333',  # "seller_1@mail.ru"
         'quantity': 5,
         'price': 10000,
         'catalog_id': [1],
         'product_id': 1
         }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
