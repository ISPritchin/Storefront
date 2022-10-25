from django_filters import rest_framework as filters

from store.models import Collection, Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'unit_price': ['lte', 'gte']
        }

    collection = filters.ModelMultipleChoiceFilter(queryset=Collection.objects.all())