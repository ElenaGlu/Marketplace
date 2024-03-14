from django.contrib import admin
from django.urls import path

from buyer import views as b
from seller import views as s

urlpatterns = [
    path('buyer_register/', b.buyer_register, name='buyer_register'),
    path('buyer_repeat_notification/', b.buyer_repeat_notification, name='buyer_repeat_notification'),
    path('buyer_confirm_email/', b.buyer_confirm_email, name='buyer_confirm_email'),
    path('buyer_login/', b.buyer_login, name='buyer_login'),
    path('buyer_redirect_reset/', b.buyer_redirect_reset, name='buyer_redirect_reset'),
    path('buyer_reset_password/', b.buyer_reset_password, name='buyer_reset_password'),
    path('buyer_logout/', b.buyer_logout, name='buyer_logout'),
    path('buyer_update_profile/', b.buyer_update_profile, name='buyer_update_profile'),
    path('buyer_update_pwd/', b.buyer_update_pwd, name='buyer_update_pwd'),
    path('buyer_provide_catalogs/', b.buyer_provide_catalogs, name='buyer_provide_catalogs'),
    path('buyer_catalog/', b.buyer_selects_products_by_category, name='buyer_selects_products_by_category'),
    path('buyer_product/', b.buyer_detail_product, name='buyer_detail_product'),
    path('buyer_add_cart/', b.buyer_add_cart, name='buyer_add_cart'),
    path('buyer_change_cart/', b.buyer_change_cart, name='buyer_change_cart'),
    path('buyer_remove_cart/', b.buyer_remove_cart, name='buyer_remove_cart'),



    path('seller_register/', s.seller_register, name='seller_register'),
    path('seller_repeat_notification/', s.seller_repeat_notification, name='seller_repeat_notification'),
    path('seller_confirm_email/', s.seller_confirm_email, name='seller_confirm_email'),
    path('seller_login/', s.seller_login, name='seller_login'),
    path('seller_redirect_reset/', s.seller_redirect_reset, name='seller_redirect_reset'),
    path('seller_reset_password/', s.seller_reset_password, name='seller_reset_password'),
    path('seller_logout/', s.seller_logout, name='seller_logout'),
    path('seller_update_profile/', s.seller_update_profile, name='seller_update_profile'),
    path('seller_update_pwd/', s.seller_update_pwd, name='seller_update_pwd'),
    path('seller_load_product/', s.seller_load_product, name='seller_load_product'),
    path('seller_change_product/', s.seller_change_product, name='seller_change_product'),
    path('seller_archive_product/', s.seller_archive_product, name='seller_archive_product'),

    path('admin/', admin.site.urls),
]
