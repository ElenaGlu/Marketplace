from django.db import models

from seller.models import Product


class Email(models.Model):
    email = models.EmailField(max_length=254)


class ProfileBuyer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    email = models.OneToOneField(Email, on_delete=models.CASCADE)
    active_account = models.BooleanField(default=False)
    shop = models.ManyToManyField(Product, through="Order")


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(ProfileBuyer, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
