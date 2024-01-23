from django.contrib import admin
from django.urls import path


from buyer import views as b
from seller import views as s


urlpatterns = [
    path('repeat_notification/', b.repeat_notification, name='repeat_notification'),
    path('confirm_email/', b.confirm_email, name='confirm_email'),
    path('shopping_cart/', b.add_in_shop_cart, name='add_in_shop_cart'),
    path('product/', b.get_detail_product, name='get_detail_product'),
    path('catalog/', b.get_product_from_catalog, name='get_product_from_catalog'),
    path('register/', b.register, name='register'),
    path('login/', b.login, name='login'),

    path('seller_register/', s.seller_register, name='seller_register'),

    path('admin/', admin.site.urls),
]
