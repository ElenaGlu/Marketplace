import json

from django.http import HttpRequest, HttpResponse

from buyer.models import Emails
from buyer.models import ProfileBuyer


def register(request: HttpRequest) -> HttpResponse:
    """
    Registers new users in the system.
    :param request: JSON object containing strings: email, name, surname, password.
    :return: "created" (201) response code
    :raises ValueError: if the user is registered in the system
    """
    if request.method == "POST":
        user_data = json.loads(request.body)
        user_email = user_data['email']
        user = Emails.objects.filter(email=user_email).first()
        if user:
            if ProfileBuyer.objects.filter(email=user_email).first():
                raise ValueError('Пользователь уже зарегистрирован')
        else:
            user = Emails.objects.create(email=user_email)
        ProfileBuyer.objects.create(email=user, name=user_data['name'],
                                    surname=user_data['surname'], password=user_data['password'])
        return HttpResponse(status=201)
