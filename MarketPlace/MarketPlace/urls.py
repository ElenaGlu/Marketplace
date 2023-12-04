from django.contrib import admin
from django.urls import path

from buyer import views

urlpatterns = [
    path('catalog/', views.get_products_from_catalog, name='get_products_from_catalog'),
    path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]
