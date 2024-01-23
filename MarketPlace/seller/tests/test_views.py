import json

from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_register(client, fixture_profile_seller):
    url = reverse('seller_register')
    data = json.dumps({
        'email': 'shishalovae@mail.ru',
        'store_name': 'store',
        'Individual_Taxpayer_Number': '12345',
        'type_of_organization': 'ИП',
        'country_of_registration': 'RU',
        'password': 'password'}
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
