import json

from rest_framework import status
from rest_framework.response import Response

from models import Emails
from models import ProfileBuyer


def register(request: json):
    user_email = request['email']
    if Emails.objects.filter(email=user_email):
        if ProfileBuyer.objects.filter(email=user_email):
            raise ValueError('Пользователь уже зарегистрирован')
        else:
            user_id = Emails.objects.get(email=user_email)
            ProfileBuyer.objects.create(email=user_id, name=request['name'],
                                        surname=request['surname'], password=request['password'])
            return Response(status=status.HTTP_201_CREATED)
    else:
        user = Emails.objects.create(email=request['email'])
        ProfileBuyer.objects.create(email=user.id, name=request['name'],
                                    surname=request['surname'], password=request['password'])
        return Response(status=status.HTTP_201_CREATED)
