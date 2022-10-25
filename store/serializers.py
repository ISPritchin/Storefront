from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.SerializerMethodField(method_name='calculate_products_count')

    def calculate_products_count(self, collection: Collection):
        return collection.products.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'collection', 'price_with_tax', ]

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # collection = CollectionSerializer()
    # collection_link = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail',
    #     source='collection'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
