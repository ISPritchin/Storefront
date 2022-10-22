from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Q, F

from store.models import Product, OrderItem

def say_hello(request: HttpRequest) -> HttpResponse:
    ids = OrderItem.objects.values('product_id').distinct()
    query_set = Product.objects.filter(id__in=ids)

    return render(request, 'hello.html', context={
        "name": "Ivan",
        "products": list(query_set)
    })