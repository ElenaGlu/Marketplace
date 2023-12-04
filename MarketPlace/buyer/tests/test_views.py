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
def create_data_db():
    data = [
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
    lst = []
    for item in data:
        lst.append(models.Catalog(title_catalog=item['fields']['title_catalog']))
    models.Catalog.objects.bulk_create(lst)


@pytest.mark.django_db
def test_get_products_from_catalog(client, create_data_db):
    url = reverse('get_products_from_catalog')
    data = json.dumps({'title_catalog': '1'})

    response = client.post(url, data, content_type='application/json')
