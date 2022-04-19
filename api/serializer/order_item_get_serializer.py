from rest_framework import serializers
from products.models import BoxProduct, OrderItem
from api.serializers import ProductSerializer


class BoxProductGetSerializer(serializers.ModelSerializer):
  orderFlavor = serializers.StringRelatedField(read_only=True)

  class Meta:
    model = BoxProduct
    fields = "__all__"


class OrderItemGetSerializer(serializers.ModelSerializer):
  product = ProductSerializer(read_only=True)
  orderFlavorCoverage = serializers.StringRelatedField(read_only=True)
  orderFlavorBizcocho = serializers.StringRelatedField(read_only=True)
  orderFlavor = serializers.StringRelatedField(read_only=True)
  box_product = BoxProductGetSerializer(many=True, read_only=True)

  class Meta:
    model = OrderItem
    fields = "__all__"
