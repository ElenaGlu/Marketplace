from django.contrib import admin

from seller.models import ProfileSeller, TokenSeller, TokenEmailSeller, Catalog, Product, CatalogProduct

admin.site.register(ProfileSeller)
admin.site.register(TokenSeller)
admin.site.register(TokenEmailSeller)
admin.site.register(Catalog)
admin.site.register(Product)
admin.site.register(CatalogProduct)
