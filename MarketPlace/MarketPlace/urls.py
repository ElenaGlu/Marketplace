from django.contrib import admin
from django.urls import path

from buyer import views

urlpatterns = [
    path('repeat_notification/', views.repeat_notification, name='repeat_notification'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('shopping_cart/', views.add_in_shop_cart, name='add_in_shop_cart'),
    path('product/', views.get_detail_product, name='get_detail_product'),
    path('catalog/', views.get_product_from_catalog, name='get_product_from_catalog'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]
