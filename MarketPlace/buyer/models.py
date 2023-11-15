from django.db import models


class Emails(models.Model):
    email = models.CharField(max_length=150)


class Profile(models.Model):
    BUYER_PROFILE = 1
    SELLER_PROFILE = 2
    PROFILE_CHOICES = (
        (BUYER_PROFILE, 'Buyer'),
        (SELLER_PROFILE, 'Seller'),
    )
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.ForeignKey(Emails, on_delete=models.CASCADE)
    profile = models.IntegerField(choices=PROFILE_CHOICES)
