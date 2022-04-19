from django.contrib import admin

from products.models import (
  CategoriaProd,
  Customer,
  BoxProduct,
  Flavor,
  FlavorBizcocho,
  FlavorCoverage,
  Order, OrderItem,
  Product,
  ShippingAddress
)


class FlavorAdmin(admin.ModelAdmin):
  list_display = ("id", "flavor")


admin.site.register(Customer)
admin.site.register(CategoriaProd)
admin.site.register(BoxProduct)

admin.site.register(Flavor, FlavorAdmin)
admin.site.register(FlavorBizcocho)
admin.site.register(FlavorCoverage)
admin.site.register(Product)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
