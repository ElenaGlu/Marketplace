from django.contrib import admin
from django.urls import path


from buyer import views as b
from seller import views as s


urlpatterns = [
    path('buyer_register/', b.buyer_register, name='buyer_register'),
    path('buyer_repeat_notification/', b.buyer_repeat_notification, name='buyer_repeat_notification'),
    path('buyer_confirm_email/', b.buyer_confirm_email, name='buyer_confirm_email'),
    path('buyer_login/', b.buyer_login, name='buyer_login'),
    # path('buyer_reset_password/', b.buyer_reset_password, name='buyer_reset_password'),
    path('buyer_provide_catalogs/', b.buyer_provide_catalogs, name='buyer_provide_catalogs'),
    path('buyer_catalog/', b.buyer_selects_products_by_category, name='buyer_selects_products_by_category'),
    path('buyer_product/', b.buyer_detail_product, name='buyer_detail_product'),
    path('buyer_add_cart/', b.buyer_add_cart, name='buyer_add_cart'),



    path('seller_register/', s.seller_register, name='seller_register'),
    path('seller_repeat_notification/', s.seller_repeat_notification, name='seller_repeat_notification'),
    path('seller_confirm_email/', s.seller_confirm_email, name='seller_confirm_email'),
    path('seller_login/', s.seller_login, name='seller_login'),
    path('seller_load_product/', s.seller_load_product, name='seller_load_product'),
    path('seller_change_product/', s.seller_change_product, name='seller_change_product'),

    path('admin/', admin.site.urls),
]
