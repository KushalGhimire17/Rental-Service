from django.contrib import admin
from products.models import Product, ProductMultipleImage, Category, Message, ProductOverview, FeaturedProduct

from .models import BookProduct

admin.site.register(BookProduct)

class ProductMultipleImageAdmin(admin.StackedInline):
    model = ProductMultipleImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductMultipleImageAdmin]

    class Meta:
        model = Product

@admin.register(ProductMultipleImage)
class ProductMultipleImageAdmin(admin.ModelAdmin):
    pass


class ProductOverViewAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'product')

admin.site.register(ProductOverview, ProductOverViewAdmin)

class FeturedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')

admin.site.register(FeaturedProduct, FeturedProductAdmin)


admin.site.register(Category)
admin.site.register(Message)
