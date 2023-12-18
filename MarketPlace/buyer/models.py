from django.db import models

from seller.models import Product


class Email(models.Model):
    email = models.EmailField(max_length=254)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    active_account = models.BooleanField(default=False)


class Token(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    token = models.CharField()


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.OneToOneField(ProfileBuyer, on_delete=models.CASCADE)
