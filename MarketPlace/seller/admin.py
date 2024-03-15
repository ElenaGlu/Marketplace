from django.contrib import admin

from seller.models import ProfileSeller, Catalog, Product, CatalogProduct

admin.site.register(ProfileSeller)
admin.site.register(Catalog)
admin.site.register(Product)
admin.site.register(CatalogProduct)
