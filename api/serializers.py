
from rest_framework import serializers
from products.models import Product, FlavorCoverage, FlavorBizcocho, Customer, CategoriaProd
from api.serializer.flavor_serializer import FlavorSerializer


class FlavorCoverageSerializer(serializers.ModelSerializer):
  class Meta:
    model = FlavorCoverage
    fields = ["id", "flavor"]


class FlavorBizcochoSerializer(serializers.ModelSerializer):
  class Meta:
    model = FlavorBizcocho
    fields = ["id", "flavor"]


class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = CategoriaProd
    fields = ["code"]


class ProductSerializer(serializers.ModelSerializer):
  flavor = FlavorSerializer(many=True, read_only=True)
  flavorCoverage = FlavorCoverageSerializer(many=True, read_only=True)
  flavorBizcocho = FlavorBizcochoSerializer(many=True, read_only=True)
  categoria = CategorySerializer(read_only=True)
  image_1 = serializers.SerializerMethodField('get_image_url_1')
  image_2 = serializers.SerializerMethodField('get_image_url_2')
  image_3 = serializers.SerializerMethodField('get_image_url_3')
  image_4 = serializers.SerializerMethodField('get_image_url_4')
  image_5 = serializers.SerializerMethodField('get_image_url_5')

  class Meta:
    model = Product
    fields = "__all__"

  def get_image_url_1(self, obj):
    if hasattr(obj.image_1, "url"):
      return obj.image_1.url

  def get_image_url_2(self, obj):
    if hasattr(obj.image_2, "url"):
      return obj.image_2.url

  def get_image_url_3(self, obj):
    if hasattr(obj.image_3, "url"):
      return obj.image_3.url

  def get_image_url_4(self, obj):
    if hasattr(obj.image_4, "url"):
      return obj.image_4.url

  def get_image_url_5(self, obj):
    if hasattr(obj.image_5, "url"):
      return obj.image_5.url

  # def to_representation(self, instance):
  #  rep = super().to_representation(instance)
  #  rep['orderFlavorCoverage'] = FlavorCoverageSerializer(
  #      instance.orderFlavorCoverage).data
  #  return rep

  #  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  #order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  #quantity = models.IntegerField(default=0, null=True, blank=True)
  # orderFlavorCoverage = models.ForeignKey(
  #    FlavorCoverage, on_delete=models.CASCADE)
  # orderFlavorBizcocho = models.ForeignKey(
  #    FlavorBizcocho, on_delete=models.CASCADE)
  #orderFlavor = models.ForeignKey(Flavor, on_delete=models.CASCADE)
  #date_added = models.DateTimeField(auto_now_add=True)
