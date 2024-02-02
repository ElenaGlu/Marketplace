from django.db import models

from seller.models import Product


class Email(models.Model):
    email = models.EmailField(max_length=254)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    email = models.OneToOneField(Email, on_delete=models.CASCADE)
    active_account = models.BooleanField(default=False)


class TokenBuyer(models.Model):
    profile = models.ForeignKey(ProfileBuyer, on_delete=models.CASCADE)
    token = models.CharField()
    stop_date = models.DateTimeField(default=None)


class TokenEmailBuyer(models.Model):
    profile = models.ForeignKey(ProfileBuyer, on_delete=models.CASCADE)
    token = models.CharField()
    stop_date = models.DateTimeField(default=None)


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.OneToOneField(ProfileBuyer, on_delete=models.CASCADE, primary_key=True)
    quantity = models.IntegerField(default=None)
