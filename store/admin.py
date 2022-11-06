from django.contrib import admin
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name:
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"')
        return ""


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }

    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'Low' if product.inventory < 10 else 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully update'
        )

    class Media:
        css = {
            'all': ['store/styles.css']
        }

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') \
              + '?' \
              + urlencode({
            'collection_id': collection.id
        })
        return format_html(f'<a href="{url}">{collection.products_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )
