import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_view_register(client):
    url = reverse('register')
    data = json.dumps({'email': 'john@mail.ru', 'name': 'john',
                       'surname': 'piter', 'password': '123'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201

    with pytest.raises(ValueError):
        client.post(url, data, content_type='application/json')


@pytest.mark.django_db
def test_view_login(client):

    create(username='john', email='john@mail.ru', password='123')

    url = reverse('login')
    data = json.dumps({'email': 'john@mail.ru', 'password': '123'})
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200

    # with pytest.raises(ValueError):
    #     data = json.dumps({'email': 'aa@mail.ru', 'password': '123'})
    #     client.post(url, data, content_type='application/json')
