""" django test """
from django.test import TestCase
from products.models import CategoriaProd


class CategoriaProdTest(TestCase):
  """ Test para el modelo OrderItem """

  def setUp(self) -> None:
    CategoriaProd.objects.create(nombre="kekes")

  def test_create_categoria_of_products(self):
    """ test crear una categoria de productos en la DB """
    categoria = CategoriaProd.objects.get(nombre='kekes')
    self.assertEqual(
        categoria.__str__(), "kekes"
    )
