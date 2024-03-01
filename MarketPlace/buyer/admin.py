from django.contrib import admin
from .models import Email, ProfileBuyer, TokenBuyer, TokenEmailBuyer, ShoppingCart

admin.site.register(Email)
admin.site.register(ProfileBuyer)
admin.site.register(TokenBuyer)
admin.site.register(TokenEmailBuyer)
admin.site.register(ShoppingCart)
