from rest_framework import serializers
from products.models import BoxProduct, OrderItem


class BoxProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = BoxProduct
    fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
  box_product = BoxProductSerializer(many=True, read_only=True)

  class Meta:
    model = OrderItem
    fields = "__all__"
