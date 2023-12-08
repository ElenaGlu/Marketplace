from django.contrib import admin
from django.urls import path

from buyer import views

urlpatterns = [
    path('product/', views.get_detail_product, name='get_detail_product'),
    path('catalog/', views.get_product_from_catalog, name='get_product_from_catalog'),
    path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]
