from django.contrib import admin
from django.urls import path

from buyer import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]
