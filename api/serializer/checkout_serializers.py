from rest_framework import serializers
from products.models import Product, OrderItem


class ProductSerializer(serializers.ModelSerializer):
  image_1 = serializers.SerializerMethodField('get_image_url_1')

  class Meta:
    model = Product
    fields = ["id", "name", "price", "image_1"]

  def get_image_url_1(self, obj):
    if hasattr(obj.image_1, "url"):
      return obj.image_1.url


class CheckoutSerializer(serializers.ModelSerializer):
  product = ProductSerializer(read_only=True)
  orderFlavorCoverage = serializers.StringRelatedField(read_only=True)
  orderFlavorBizcocho = serializers.StringRelatedField(read_only=True)
  orderFlavor = serializers.StringRelatedField(read_only=True)

  class Meta:
    model = OrderItem
    fields = "__all__"
