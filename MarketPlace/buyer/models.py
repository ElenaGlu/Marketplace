from django.db import models


class Emails(models.Model):
    email = models.CharField(max_length=150)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.ForeignKey(Emails, on_delete=models.CASCADE)
