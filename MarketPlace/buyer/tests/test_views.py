import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_view_register(client):
    url = reverse('register')
    response = client.post(
        url,
        data=json.dumps({'email': 'john@mail.ru', 'name': 'john',
                         'surname': 'Piter', 'password': '123'}),
        content_type='application/json')
    assert response.status_code == 201
