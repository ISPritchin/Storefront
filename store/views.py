from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(APIView):
    def get(self, request: HttpRequest):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset,
                                       many=True,
                                       context={'request': request})
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request: HttpRequest, id: int) -> Response:
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request: HttpRequest, id: int) -> Response:
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: HttpRequest, id: int) -> Response:
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            error_message = 'product cannot be deleted because it is assosiated with an order item'
            return Response({'error': error_message}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request: HttpRequest) -> Response:
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.all(), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.all(), pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: HttpRequest, pk: int) -> Response:
        collection = get_object_or_404(Collection.objects.all(), pk=pk)
        if collection.products.count() > 0:
            error_message = 'collection cannot be deleted because it include one or more products'
            return Response({'error': error_message}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
