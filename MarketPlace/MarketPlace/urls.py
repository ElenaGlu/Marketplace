from django.contrib import admin
from django.urls import path


from buyer import views as b
from seller import views as s


urlpatterns = [
    path('buyer_register/', b.buyer_register, name='buyer_register'),
    path('buyer_repeat_notification/', b.buyer_repeat_notification, name='buyer_repeat_notification'),
    path('buyer_confirm_email/', b.buyer_confirm_email, name='buyer_confirm_email'),
    path('buyer_login/', b.buyer_login, name='buyer_login'),
    path('catalog/', b.get_product_from_catalog, name='get_product_from_catalog'),
    path('product/', b.get_detail_product, name='get_detail_product'),
    path('shopping_cart/', b.add_in_shop_cart, name='add_in_shop_cart'),



    path('seller_register/', s.seller_register, name='seller_register'),
    path('seller_repeat_notification/', s.seller_repeat_notification, name='seller_repeat_notification'),
    path('seller_confirm_email/', s.seller_confirm_email, name='seller_confirm_email'),
    path('seller_login/', s.seller_login, name='seller_login'),

    path('admin/', admin.site.urls),
]
