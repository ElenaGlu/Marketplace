from django.db import models


class Emails(models.Model):
    email = models.CharField(max_length=50)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.ForeignKey(Emails, on_delete=models.CASCADE)
