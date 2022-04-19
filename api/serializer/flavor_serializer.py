
from rest_framework import serializers
from products.models import Flavor


class FlavorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Flavor
    fields = ["id", "flavor"]
