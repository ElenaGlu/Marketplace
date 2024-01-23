from django.http import HttpResponse

from buyer.models import Email, TokenEmail
from buyer.utils.auth import create_token, create_hash, send_notification
from seller.models import ProfileSeller


class SellerAuth:

    @staticmethod
    def user_register(user_data):
        user_email = user_data['email']
        email = Email.objects.filter(email=user_email).first()
        if email:
            if ProfileSeller.objects.filter(email=email).first():
                raise ValueError('the user is already registered')
        else:
            email = Email.objects.create(email=user_email)

            data_token = create_token()
            token = data_token['token']
            TokenEmail.objects.create(
                email=email,
                token_email=token,
                stop_date=data_token['stop_date'])

            password_hash = create_hash(user_data['password'])
            ProfileSeller.objects.create(
                email=email,
                store_name=user_data['store_name'],
                Individual_Taxpayer_Number=user_data['Individual_Taxpayer_Number'],
                type_of_organization=user_data['type_of_organization'],
                country_of_registration=user_data['country_of_registration'],
                password=password_hash
            )

            send_notification([user_email], f'http://localhost/confirm/?token={token}')
        return HttpResponse(status=201)