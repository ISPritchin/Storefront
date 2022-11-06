from rest_framework_nested import routers
from . import views

main_router = routers.DefaultRouter()
main_router.register('products', views.ProductViewSet, basename='products')
main_router.register('collections', views.CollectionViewSet)
main_router.register('carts', views.CartViewSet)
main_router.register('customers', views.CustomerViewSet)
main_router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(
    main_router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')
products_router.register(
    'images', views.ProductImageViewSet, basename='product-images')

carts_router = routers.NestedDefaultRouter(main_router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = main_router.urls + products_router.urls + carts_router.urls
