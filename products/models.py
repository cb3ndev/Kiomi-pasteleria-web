from django.db import models

from django.contrib.auth.models import User
# Validador para los campos integers, se uso en el model de orderitems
from django.core.validators import MaxValueValidator, MinValueValidator
from shortuuid.django_fields import ShortUUIDField
from cloudinary.models import CloudinaryField


class Customer(models.Model):
  """
  Cliente
  """
  user = models.OneToOneField(
      User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  lastName = models.CharField(max_length=200, null=True)
  email = models.EmailField(max_length=200, null=True)

  class Meta:
    verbose_name = "Customer"
    verbose_name_plural = "Customers"
    ordering = ["user"]

  def __str__(self):
    return self.name


# Por el momento solo se han modificado el product y la categoriaProd
class CategoriaProd(models.Model):  # categoria del producto (galleta, torta, etc.)
  """
  Partes de un producto como cobertor, bizcocho, etc
  code:
    tortas -> '1'
    galletas -> '2'
    otros -> '3'
  """
  nombre = models.CharField(max_length=50)
  code = models.CharField(max_length=50)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.nombre


class Product(models.Model):
  """
  Partes de un producto como cobertor, bizcocho, etc
  """

  name = models.CharField(max_length=100)
  price = models.FloatField()
  description = models.CharField(max_length=1000)
  categoria = models.ForeignKey(
      CategoriaProd, on_delete=models.CASCADE, related_name="categoria")
  image_1 = CloudinaryField("kiomi", null=True, blank=True)
  image_2 = CloudinaryField("kiomi", null=True, blank=True)
  image_3 = CloudinaryField("kiomi", null=True, blank=True)
  image_4 = CloudinaryField("kiomi", null=True, blank=True)
  image_5 = CloudinaryField("kiomi", null=True, blank=True)

  class Meta:
    verbose_name = "Product"
    verbose_name_plural = "Products"
    ordering = ["name"]

  def __str__(self) -> str:
    return self.name

  def save(self, *args, **kwargs):
    self.price = round(self.price, 2)
    super(Product, self).save(*args, **kwargs)


class FlavorBizcocho(models.Model):
  """
  Sabores de los productos
  """

  flavor = models.CharField("Sabor de bizcocho", max_length=50)
  product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      related_name="flavorBizcocho",
      blank=True,
      null=True,
  )

  def __str__(self) -> str:
    return self.flavor


class FlavorCoverage(models.Model):
  """
  Sabores de los productos
  """

  flavor = models.CharField("Sabor de cobertura", max_length=50)
  product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      related_name="flavorCoverage",
      blank=True,
      null=True,
  )

  def __str__(self) -> str:
    return self.flavor


class Flavor(models.Model):
  """
  Sabores de los productos
  """

  flavor = models.CharField("Sabor", max_length=50)
  product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      related_name="flavor",
      blank=True,
      null=True,
  )

  def __str__(self) -> str:
    return self.flavor


class Order(models.Model):
  customer = models.ForeignKey(
      Customer, on_delete=models.SET_NULL, null=True, blank=True
  )
  date_ordered = models.DateTimeField(auto_now_add=True)
  # el campo complete consiste en lo siguiente:
  # complete =0, compra incompleta o rechazada
  # complete = 1, compra completa y aceptada
  # complete = 2, compra pendiente de confirmar por el vendedor pero aceptada hacia el cliente (yape o plin)
  complete = models.IntegerField(default=0, null=True, blank=False)
  orderUniqueIdentifier = ShortUUIDField(
      length=8,
      max_length=12,
      alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789",
  )
  metodoPago = models.CharField(max_length=30, null=True)
  nombrePagadorFull = models.CharField(max_length=100, null=True)
  date_delivery = models.DateField(null=True, blank=False)

  class Meta:
    verbose_name = "order"
    verbose_name_plural = "orders"
    ordering = ["date_ordered"]

  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total

  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total

  # Antes las tortas valian 2 pero ese pedido quedo obsoleto por tanto  "get_cart_items_calendar" quedo obsoleto y
  # se usara get_cart_items
  @property
  def get_cart_items_calendar(self):
    orderitems = self.orderitem_set.all()
    total = 0
    for item in orderitems:
      categoria = item.product.categoria.code
      print(categoria)
      if categoria == "1":
        total += (item.quantity)*2
      else:
        total += item.quantity
    return total

  def __str__(self):
    return str(self.orderUniqueIdentifier)


class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  quantity = models.PositiveIntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, blank=True,)
  orderFlavorCoverage = models.ForeignKey(
      FlavorCoverage, null=True, blank=True, on_delete=models.CASCADE)
  orderFlavorBizcocho = models.ForeignKey(
      FlavorBizcocho, null=True, blank=True, on_delete=models.CASCADE)
  orderFlavor = models.ForeignKey(
      Flavor, null=True, blank=True, on_delete=models.CASCADE)
  date_added = models.DateTimeField(auto_now_add=True)
  validateOrderItem = models.BooleanField(default=False)

  class Meta:
    verbose_name = "orderitem"
    verbose_name_plural = "orderitems"
    ordering = ["id"]

  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total

  def __str__(self):
    return str(self.product)


class BoxProduct(models.Model):
  """
    Box of a product
  """
  order_item = models.ForeignKey(
      OrderItem,
      on_delete=models.CASCADE,
      null=True,
      blank=True,
      related_name="box_product"
  )
  quantity = models.IntegerField()
  orderFlavor = models.ForeignKey(
      Flavor, null=True, blank=True, on_delete=models.CASCADE)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return str(self.id)


class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
  order = models.OneToOneField(
      Order, on_delete=models.SET_NULL, null=True, related_name="shippingAddress")
  nombrePersonaEnvio = models.CharField(max_length=200, null=False)
  address = models.CharField(max_length=200, null=False)
  distrito = models.CharField(max_length=200, null=False)
  phoneNumber = models.PositiveIntegerField(null=False)
  reference = models.CharField(max_length=200, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = "shippingaddress"
    verbose_name_plural = "shippingaddresses"
    ordering = ["id"]

  def __str__(self):
    return self.address
