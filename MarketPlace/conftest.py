import datetime

import pytest

from buyer import models as b_models
from config import EMAIL_1, EMAIL_2
from seller import models as s_models
from utils.access import Access


@pytest.fixture()
def fixture_email():
    email = [
        "seller_1@mail.ru",
        "seller_2@mail.ru",
        EMAIL_1,
        EMAIL_2,
        "buyer_1@mail.ru"
    ]
    temporary = []
    for obj in email:
        temporary.append(b_models.Email(email=obj))
    return b_models.Email.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_profile_seller(fixture_email):
    password_hash = Access.create_hash('1')
    profile_seller = [
        {"id": 2,
         "store_name": "seller",
         "individual_taxpayer_number": "111",
         "type_of_organization": "ИП",
         "country_of_registration": "RU",
         "password": password_hash,
         "email_id": fixture_email[2].id,  # "elena.g"
         "active_account": False
         },
        {"id": 3,
         "store_name": "seller_2",
         "individual_taxpayer_number": "222",
         "type_of_organization": "ИП",
         "country_of_registration": "RU",
         "password": password_hash,
         "email_id": fixture_email[1].id,  # "seller_2@mail.ru"
         "active_account": True
         },
        {"id": 4,
         "store_name": "seller_1",
         "individual_taxpayer_number": "111",
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
    for idx, obj in enumerate(catalog):
        temporary.append(s_models.Catalog(id=idx + 1, title_catalog=obj))
    return s_models.Catalog.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_product(fixture_catalog, fixture_profile_seller):
    product = [
        {"id": 2,
         "store_name_id": fixture_profile_seller[0].id,  # "seller_1"
         "title_product": "computer table",
         "description": "size:1500",
         "quantity": 10,
         "price": 1999,
         },
        {"id": 3,
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
            "id": 4,
            "product_id": fixture_product[0].id,
            "catalog_id": fixture_catalog[0].id
        },
        {
            "id": 5,
            "product_id": fixture_product[0].id,
            "catalog_id": fixture_catalog[1].id
        },
        {
            "id": 6,
            "product_id": fixture_product[1].id,
            "catalog_id": fixture_catalog[0].id
        }
    ]
    temporary = []
    for obj in catalog_product:
        temporary.append(s_models.CatalogProduct(**obj))
    return s_models.CatalogProduct.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_profile_buyer(fixture_email):
    password_hash = Access.create_hash('1')
    profile_buyer = [
        {
            "name": "elena",
            "surname": "test_user",
            "password": password_hash,
            "email_id": fixture_email[2].id,  # "elena.g"
            "active_account": False
        },
        {
            "name": "buyer_2",
            "surname": "test",
            "password": password_hash,
            "email_id": fixture_email[3].id,  # "shi"
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
            "profile": fixture_profile_buyer[0],  # "elena.g"
            "stop_date": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
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
            "profile": fixture_profile_seller[0],  # "elena.g"
            "stop_date": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }
    ]
    temporary = []
    for obj in token:
        temporary.append(s_models.TokenEmailSeller(**obj))
    return s_models.TokenEmailSeller.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_token_buyer(fixture_profile_buyer):
    token = [
        {   "id": 1,
            "token": "111",
            "profile": fixture_profile_buyer[1],  # "shi"
            "stop_date": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        },
        {"id": 2,
            "token": "222",
            "profile": fixture_profile_buyer[2],  # "buyer_1@mail.ru"
            "stop_date": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }
    ]
    temporary = []
    for obj in token:
        temporary.append(b_models.TokenBuyer(**obj))
    return b_models.TokenBuyer.objects.bulk_create(temporary)


@pytest.fixture()
def fixture_token_seller(fixture_profile_seller):
    token = [
        {"id": 1,
         "token": "333",
         "profile": fixture_profile_seller[2],  # "seller_1@mail.ru"
         "stop_date": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
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
        {"id": 2,
         "product_id": fixture_product[0].id,
         "buyer_id": fixture_profile_buyer[1].id,  # "shi"
         "quantity": 2
         },
        {"id": 3,
         "product_id": fixture_product[0].id,
         "buyer_id": fixture_profile_buyer[2].id,  # "buyer_1@mail.ru"
         "quantity": 4
         }
    ]
    temporary = []
    for obj in shopping_cart:
        temporary.append(b_models.ShoppingCart(**obj))
    return b_models.ShoppingCart.objects.bulk_create(temporary)
