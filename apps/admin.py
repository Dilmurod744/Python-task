from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from apps.filters import PriceRangeFilter
from apps.models import Category, Product, ProductImage, Shop
from apps.resources import ProductModelResource


@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = ("id", "title",)
    search_fields = ("id", "title", "parent__title",)


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = ('id', 'title', 'description', 'image_show')
    search_fields = ['id', 'title', ]
    list_per_page = 10
    list_max_show_all = 20

    def image_show(self, obj: Shop):
        if obj.image:
            return mark_safe("<img src='{}' width='200' />".format(obj.image.url))

        return ''

    image_show.description = 'image'


class ProductImageStackedInline(StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0
    fields = ['image']
    list_filter = (PriceRangeFilter,)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    inlines = (ProductImageStackedInline,)
    list_display = ['id', 'description', 'title', 'amount', 'price', 'active', 'image_show']
    search_fields = ['id', 'title']
    list_per_page = 10
    list_max_show_all = 20
    resource_class = ProductModelResource

    def image_show(self, obj: Product):
        if obj.product_images.first():
            return mark_safe("<img src='{}' width='200' />".format(obj.product_images.first().image.url))

        return ''

    image_show.description = 'images'
