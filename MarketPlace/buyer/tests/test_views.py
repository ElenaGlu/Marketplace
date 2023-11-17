import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_view_register(client):
    url = reverse('register')
    response = client.post(url, data={"email": "john@mail.ru", "name": "john", "surname": "Piter", "password": "123"})
    assert response.status_code == 401
