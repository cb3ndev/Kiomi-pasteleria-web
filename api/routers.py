from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from api.views import ProcessOrderViewSet, ProductViewSet, ProductDetailViewSet, OrderItemGetViewSet, OrderItemPostViewSet, CheckoutViewSet, CustomerViewSet, ValidateShipping,DatePicker
router = DefaultRouter()

router.register(
    r'products',
    ProductViewSet,
    basename="products"
)
router.register(
    r'products-detail',
    ProductDetailViewSet,
    basename="products-details"
)

router.register(
    r'order-item-get',
    OrderItemGetViewSet,
    basename="order-item-get"
)

router.register(
    r'order-item-post',
    OrderItemPostViewSet,
    basename="order-item-post"
)

router.register(
    r'checkout',
    CheckoutViewSet,
    basename="checkout"
)

router.register(
    r'process-order',
    ProcessOrderViewSet,
    basename="process-order"
)

router.register(
    r'customer',
    CustomerViewSet,
    basename="customer"
)

router.register(
    r'validate-shipping',
    ValidateShipping,
    basename="validate-shipping"
)

router.register(
    r'Date-Picker',
    DatePicker,
    basename="Date-Picker"
)

urlpatterns = router.urls
