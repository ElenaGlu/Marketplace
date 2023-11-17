import json

from django.http import HttpRequest, HttpResponse

from buyer.models import Emails
from buyer.models import ProfileBuyer


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data_register = json.loads(request.body)
        user_email = data_register['email']
        user = Emails.objects.filter(email=user_email).first()
        if user:
            if ProfileBuyer.objects.filter(email=user_email):
                raise ValueError('Пользователь уже зарегистрирован')
        else:
            user = Emails.objects.create(email=data_register['email'])
        ProfileBuyer.objects.create(email=user.id, name=data_register['name'],
                                    surname=data_register['surname'], password=data_register['password'])
        return HttpResponse(status=201)
