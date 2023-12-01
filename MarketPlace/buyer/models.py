from django.db import models


class Email(models.Model):
    email = models.EmailField(max_length=254)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)