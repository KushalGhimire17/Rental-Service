from django.contrib import admin
from products.models import Product, ProductMultipleImage, Category

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

admin.site.register(Category)
