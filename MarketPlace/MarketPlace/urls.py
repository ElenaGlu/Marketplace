from django.contrib import admin
from django.urls import path

from buyer import views

urlpatterns = [
    path('', views.register, name='register'),
    path('admin/', admin.site.urls),
]
