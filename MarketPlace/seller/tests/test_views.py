import json

import pytest
from django.urls import reverse

from config import EMAIL_1, EMAIL_4, TOKEN_EMAIL_S, TOKEN_S, VALID_TOKEN_S, TOKEN_SHOP_S


@pytest.mark.django_db
def test_register(client, fixture_profile_seller):
    url = reverse('seller_register')
    data = json.dumps(
        {
            'email': EMAIL_4,
            'store_name': 'store',
            'individual_taxpayer_number': '12345',
            'type_of_organization': 'ИП',
            'country_of_registration': 'RU',
            'password': 'password'
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_repeat_notification(client, fixture_profile_seller):
    url = reverse('seller_repeat_notification')
    data = json.dumps(
        {
            'email': EMAIL_1
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_confirm_email(client, fixture_profile_seller, redis_client):
    url = reverse('seller_confirm_email')
    data = {
        "token": TOKEN_EMAIL_S  # id=2
    }
    response = client.get(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login(client, fixture_profile_seller):
    url = reverse('seller_login')
    data = json.dumps(
        {
            'email': 'seller_2@mail.ru',
            'password': '1'
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_redirect_reset(client, fixture_profile_seller):
    url = reverse('seller_redirect_reset')
    data = json.dumps(
        {
            'email': EMAIL_1
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_reset_password(client, fixture_profile_seller):
    url = reverse('seller_reset_password')
    data = json.dumps(
        {
            'email': EMAIL_1,
            'password': '2'
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_logout(client, fixture_profile_seller, redis_client):
    url = reverse('seller_logout')
    data = json.dumps(
        {
            'token': TOKEN_S
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_profile(client, fixture_profile_seller, redis_client):
    url = reverse('seller_update_profile')
    data = json.dumps(
        {
            'token': VALID_TOKEN_S,
            'store_name': 'new_seller',
            'individual_taxpayer_number': '222',
            'password': 'pwd'
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_pwd(client, fixture_profile_seller, redis_client):
    url = reverse('seller_update_pwd')
    data = json.dumps(
        {
            'token': 'token',

        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_load_product(client, fixture_catalog_product, redis_client):
    url = reverse('seller_load_product')
    data = json.dumps(
        {
            'token': TOKEN_SHOP_S,
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
def test_change_product(client, fixture_catalog_product, redis_client):
    url = reverse('seller_change_product')
    data = json.dumps(
        {
            'token': TOKEN_SHOP_S,
            'quantity': 5,
            'price': 10000,
            'catalog_id': [1],
            'product_id': 3
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_archive_product(client, fixture_catalog_product, redis_client):
    url = reverse('seller_archive_product')
    data = json.dumps(
        {
            'token': TOKEN_SHOP_S,
            'product_id': 1
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
