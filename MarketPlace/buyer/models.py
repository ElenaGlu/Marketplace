from django.db import models

from seller.models import Product


class Email(models.Model):
    email = models.EmailField(max_length=254)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, default='out of stock', on_delete=models.SET_DEFAULT)
    buyer = models.OneToOneField(ProfileBuyer, on_delete=models.CASCADE)
