import datetime

import hashlib
import pytest

from seller import models as s_models
from buyer import models as b_models


@pytest.fixture()
def fixture_email():
    email = [
        "seller_1@mail.ru",
        "seller_2@mail.ru",
        "elena.g.2023@list.ru",
        "shishalova310@gmail.com",
        "buyer_1@mail.ru"
    ]
    temporary = []
    for obj in email:
        temporary.append(b_models.Email(email=obj))
    return b_models.Email.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_profile_seller(fixture_email):
    salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
    password_hash = hashlib.pbkdf2_hmac('sha256', '1'.encode('utf-8'), salt, 100000).hex()
    profile_seller = [
        {
            "store_name": "seller_1",
            "Individual_Taxpayer_Number": "111",
            "type_of_organization": "ИП",
            "country_of_registration": "RU",
            "password": password_hash,
            "email_id": fixture_email[2].id,  # "elena.g.2023@list.ru"
            "active_account": False
        },
        {
            "store_name": "seller_2",
            "Individual_Taxpayer_Number": "222",
            "type_of_organization": "ИП",
            "country_of_registration": "RU",
            "password": password_hash,
            "email_id": fixture_email[1].id,  # "seller_2@mail.ru"
            "active_account": True
        },
        {
            "store_name": "seller_1",
            "Individual_Taxpayer_Number": "111",
            "type_of_organization": "ИП",
            "country_of_registration": "RU",
            "password": password_hash,
            "email_id": fixture_email[0].id,  # "seller_1@mail.ru"
            "active_account": True
        }
    ]
    temporary = []
    for obj in profile_seller:
        temporary.append(s_models.ProfileSeller(**obj))
    return s_models.ProfileSeller.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_catalog():
    catalog = ["home", "furniture"]
    temporary = []
    for obj in catalog:
        temporary.append(s_models.Catalog(title_catalog=obj))
    return s_models.Catalog.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_product(fixture_catalog, fixture_profile_seller):
    product = [
        {
            "store_name_id": fixture_profile_seller[0].id,  # "seller_1"
            "title_product": "computer table",
            "description": "size:1500",
            "quantity": 10,
            "price": 1999,
        },
        {
            "store_name_id": fixture_profile_seller[1].id,  # "seller_2"
            "title_product": "flower",
            "description": "ficus",
            "quantity": 5,
            "price": 799,
        }
    ]
    temporary = []
    for obj in product:
        temporary.append(s_models.Product(**obj))
    return s_models.Product.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_catalog_product(fixture_product, fixture_catalog):
    catalog_product = [
        {
            "product_id": fixture_product[0].id,
            "catalog_id": fixture_catalog[0].id
        },
        {
            "product_id": fixture_product[0].id,
            "catalog_id": fixture_catalog[1].id
        },
        {
            "product_id": fixture_product[1].id,
            "catalog_id": fixture_catalog[0].id
        }
    ]
    temporary = []
    for obj in catalog_product:
        temporary.append(s_models.CatalogProduct(**obj))
    s_models.CatalogProduct.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_profile_buyer(fixture_email):
    salt = b'\xefQ\x8d\xad\x8f\xd5MR\xe1\xcb\tF \xf1t0\xb6\x02\xa9\xc09\xae\xdf\xa4\x96\xd0\xc6\xd6\x93:%\x19'
    password_hash = hashlib.pbkdf2_hmac('sha256', '1'.encode('utf-8'), salt, 100000).hex()
    profile_buyer = [
        {
            "name": "elena",
            "surname": "test_user",
            "password": password_hash,
            "email_id": fixture_email[2].id,  # "elena.g.2023@list.ru"
            "active_account": False
        },
        {
            "name": "buyer_2",
            "surname": "test",
            "password": password_hash,
            "email_id": fixture_email[3].id,  # "buyer_2@mail.ru"
            "active_account": True
        },
        {
            "name": "buyer_1",
            "surname": "test",
            "password": password_hash,
            "email_id": fixture_email[4].id,  # "buyer_1@mail.ru"
            "active_account": True
        }
    ]
    temporary = []
    for obj in profile_buyer:
        temporary.append(b_models.ProfileBuyer(**obj))
    return b_models.ProfileBuyer.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_token_email_buyer(fixture_profile_buyer):
    token = [
        {
            "token": "123",
            "profile": fixture_profile_buyer[0],  # "elena.g.2023@list.ru"
            "stop_date": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
    ]
    temporary = []
    for obj in token:
        temporary.append(b_models.TokenEmailBuyer(**obj))
    return b_models.TokenEmailBuyer.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_token_email_seller(fixture_profile_seller):
    token = [
        {
            "token": "123",
            "profile": fixture_profile_seller[0],  # "elena.g.2023@list.ru"
            "stop_date": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
    ]
    temporary = []
    for obj in token:
        temporary.append(s_models.TokenEmailSeller(**obj))
    return s_models.TokenEmailSeller.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_token_buyer(fixture_profile_buyer):
    token = [
        {
            "token": "111",
            "profile": fixture_profile_buyer[1],  # "buyer_2@mail.ru"
            "stop_date": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        {
            "token": "222",
            "profile": fixture_profile_buyer[2],  # "buyer_1@mail.ru"
            "stop_date": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
    ]
    temporary = []
    for obj in token:
        temporary.append(b_models.TokenBuyer(**obj))
    return b_models.TokenBuyer.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_token_seller(fixture_profile_seller):
    token = [
        {
            "token": "333",
            "profile": fixture_profile_seller[2],  # "seller_1@mail.ru"
            "stop_date": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
    ]
    temporary = []
    for obj in token:
        temporary.append(s_models.TokenSeller(**obj))
    return s_models.TokenSeller.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_shopping_cart(fixture_profile_buyer, fixture_product, fixture_catalog_product,
                          fixture_token_buyer):
    shopping_cart = [
        {
            "product_id": fixture_product[0].id,
            "buyer_id": fixture_profile_buyer[1].id,  # "buyer_2@mail.ru"
            "quantity": 2
        }
    ]
    temporary = []
    for obj in shopping_cart:
        temporary.append(b_models.ShoppingCart(**obj))
    return b_models.ShoppingCart.objects.bulk_create(temporary)
