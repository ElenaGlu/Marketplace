from django.db import models
from django_countries.fields import CountryField

from buyer.models import Emails


class ProfileSeller(models.Model):
    TYPE_ORGANIZATION = (
        ('ИП', 'Индивидуальный предприниматель'),
        ('ООО', 'Общество с Ограниченной Ответственностью'),
    )
    Individual_Taxpayer_Number = models.CharField(max_length=12)
    type_of_organization = models.CharField(choices=TYPE_ORGANIZATION)
    country_of_registration = CountryField()
    password = models.CharField(max_length=20)
    email = models.ForeignKey(Emails, on_delete=models.CASCADE)
