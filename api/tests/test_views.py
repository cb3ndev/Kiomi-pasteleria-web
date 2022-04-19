""" rest framework """
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import OrderItemSerializer
from products.models import OrderItem


class GetAllOrderItemsTest(APITestCase):
  """ Test for GET all order items API """

  def setUp(self) -> None:
    OrderItem.objects.create(quantity=3)
    OrderItem.objects.create(quantity=10)
    OrderItem.objects.create(quantity=20)
    OrderItem.objects.create(quantity=40)

  def test_get_all_order_items(self):
    # get api response
    res = self.client.get("/api/order-item/", format='json')
    # get data from DB
    order_items = OrderItem.objects.all()
    serializer = OrderItemSerializer(order_items, many=True)
    self.assertEqual(res.data, serializer.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)


class GetSingleOrderItemTest(APITestCase):
  """ Test for GET single order item """

  def setUp(self) -> None:
    self.order_first = OrderItem.objects.create(quantity=3)
    self.order_second = OrderItem.objects.create(quantity=10)
    self.order_third = OrderItem.objects.create(quantity=20)
    self.order_fourth = OrderItem.objects.create(quantity=50)

  def test_get_valid_single_order_item(self):
    # get api response
    res = self.client.get(
        f"/api/order-item/{self.order_second.pk}/", format='json')
    # get data from DB
    order_item = OrderItem.objects.get(pk=self.order_second.pk)
    serializer = OrderItemSerializer(order_item)
    self.assertEqual(res.data, serializer.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_get_invalid_single_order_item(self):
    # get api response
    res = self.client.get(f"/api/order-item/{9999}/", format='json')
    self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewOrderItemtest(APITestCase):
  """ Test for inserting a new order item """

  def setUp(self) -> None:
    self.valid_payload = {
        "quantiy": 4
    }
    self.invalid_payload = {
        "quantity": "uno"
    }

  def test_create_valid_order_item(self):
    # get api response
    res = self.client.post(
        "/api/order-item/", self.valid_payload, format="json"
    )
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)

  def test_create_invalid_order_item(self):
    # get api response
    res = self.client.post(
        "/api/order-item/", self.invalid_payload, format="json"
    )
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
