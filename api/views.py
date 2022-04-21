""" rest framework api """
from datetime import datetime
from urllib import response
from products.order_services import OrderServices
import mercadopago
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import render
from api.serializer.order_item_serializers import BoxProductSerializer, OrderItemSerializer
from api.serializer.order_item_get_serializer import OrderItemGetSerializer

from products.models import BoxProduct, Customer, Flavor, Order, Product, ShippingAddress, FlavorCoverage, FlavorBizcocho
from products.models import OrderItem
from api.serializers import ProductSerializer, CustomerSerializer
from api.serializer.checkout_serializers import CheckoutSerializer
import json

from dotenv import load_dotenv
import os
load_dotenv()

# import datetime


class ProductViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    pagination_class = PageNumberPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# class PostPagination(PageNumberPagination):
# 	page_size=2


class ProductDetailViewSet(viewsets.GenericViewSet):
    """
    Detalles del producto
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderItemPostViewSet(
    viewsets.GenericViewSet
):
    """
    Lista de items que el cliente añadió a su carrito (usar para POST, UPDATE y DELETE)
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OrderItemSerializer(queryset, many=True)
        # si el campo esta en false eliminar caso contrario enviar
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderItemSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print('yep request data: ', request.data)
        product_id = request.data['product']
        # get product
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(id=request.user.customer.id)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=0)
        new_data = request.data
        new_data['order'] = order.id
        print('yep new data: ', new_data)
        code = product.categoria.code
        if code == '2':
            # galleta
            # get or create order item
            quantity = request.data['quantity']
            order_item = OrderItem.objects.create(
                product=product, order=order, quantity=quantity, validateOrderItem=True)
            # get flavor
            # flavor = Flavor.objects.get(id=request.data['orderFlavor'])
            # get or create box product
            # quantity_cookies = request.data['quantityCookies']
            # box_product, created = BoxProduct.objects.get_or_create(
            #    order_item=order_item,
            #    orderFlavor=flavor,
            #    quantity=quantity_cookies
            # )
            # box_product.save()
            # inicio edit ##########3
            print(request.data['box_product'])
            for grupoGalletitas in request.data['box_product']:
                BoxProduct.objects.create(
                    order_item=order_item,
                    orderFlavor=Flavor.objects.get(id=grupoGalletitas[0]),
                    quantity=grupoGalletitas[1]
                ).save()

            # fin edit################3

            # Para serializar
            queryset = OrderItem.objects.get(id=order_item.id)
            order_item_serializer = OrderItemSerializer(queryset)
            return Response(order_item_serializer.data, status=status.HTTP_201_CREATED)
        # no es galleta
        serializer = self.get_serializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk,  *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        order_item = OrderItem.objects.get(id=pk)
        category_code = order_item.product.categoria.code
        print('yep categoria code', category_code)
        print('box_product_id' in request.data or 'orderFlavor' in request.data)
        if serializer.is_valid():
            # Se aumento algunas condiciones aqui ya que no me permitia actualizar SOLO el quantity de order items en
            # galletas, lo que se hizo es que cuando se actualiza SOLO el quantity en galletas, se salta el codigo de abajo.
            # y sigue el procedimiento normal

            if (category_code == '2' and ('box_product_id' in request.data or 'orderFlavor' in request.data)):
                # galleta
                try:
                    box_product_id = request.data['box_product_id']
                    instance_box_product = BoxProduct.objects.get(
                        id=box_product_id)
                    quantity_cookies = request.data['quantity_cookies']
                    serializer_box_product = BoxProductSerializer(
                        instance_box_product, {'quantity': quantity_cookies})
                    print('ye serializer box product: ',
                          serializer_box_product.is_valid())
                    if serializer_box_product.is_valid():
                        serializer_box_product.save()
                        # serializar update response
                        queryset = OrderItem.objects.get(id=pk)
                        order_item_serializer = OrderItemSerializer(queryset)
                        return Response(order_item_serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer_box_product.errors, status=status.HTTP_400_BAD_REQUEST)
                except:
                    flavor_id = request.data['orderFlavor']
                    # get flavor
                    flavor = Flavor.objects.get(id=flavor_id)
                    quantity_cookies = request.data['quantity_cookies']
                    box_product = BoxProduct.objects.create(
                        order_item=order_item,
                        orderFlavor=flavor,
                        quantity=quantity_cookies
                    )
                    box_product.save()
                    queryset = OrderItem.objects.get(id=pk)
                    order_item_serializer = OrderItemSerializer(queryset)
                    print(order_item_serializer.data)
                    return Response(order_item_serializer.data, status=status.HTTP_201_CREATED)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        order_item = OrderItem.objects.get(id=pk)
        category_code = order_item.product.categoria.code
        if category_code == '2':
            try:
                box_product_id = request.data['box_product_id']
                instance_box_product = BoxProduct.objects.get(
                    id=box_product_id)
                instance_box_product.delete()
                # delete cuando box product count() es igual a 0
                print('yep box product count: ',
                      order_item.box_product.count())
                count = order_item.box_product.count()
                if count == 0:
                    instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
######################


class OrderItemGetViewSet(
    viewsets.GenericViewSet
):
    """
    Lista de items que el cliente añadió a su carrito (usar para GET)
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemGetSerializer

    def list(self, request, *args, **kwargs):

        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=0
        )
        cart_items = order.get_cart_items
        items = order.orderitem_set.filter(validateOrderItem=True)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CheckoutViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=0)
        items = order.orderitem_set.all()
        serializer = CheckoutSerializer(items, many=True)
        cart_items = order.get_cart_items
        cart_total = order.get_cart_total
        orderUniqueIdentifier = order.orderUniqueIdentifier

        response = {
            "cartItems": cart_items,
            "cartTotal": cart_total,
            "items": serializer.data,
            "orderUniqueIdentifier": orderUniqueIdentifier,
        }

        return Response(response, status=status.HTTP_200_OK)


class ProcessOrderViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        # mercadopago
        print('yep request data: ', request.data)
        identificador = request.data["identificador"]
        nombrePagador = request.data["nombrePagador"]
        apellidoPagador = request.data["apellidoPagador"]
        dateDelivery = request.data["dateDelivery"]

        total = float(request.data["total"])
        # get customer
        if request.user.is_authenticated:
            customer = request.user.customer
            # get or create order with a random orderUniqueIdentifier
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
        else:
            order = Order.objects.get(
                complete=0, orderUniqueIdentifier=identificador
            )
            ##########INICIO: En esta parte se posteara los productos de la orden: ##########
            # Esto solo se hara para cuando el user no este loggeado:
            for item in request.data['items']:
                order_item = None
                if item["orderFlavor"] != None:
                    order_item = OrderItem.objects.create(
                        product=Product.objects.get(id=item["product"]),
                        order=order, quantity=item["quantity"],
                        orderFlavor=Flavor.objects.get(id=item["orderFlavor"]),
                        validateOrderItem=True)
                    order_item.save()
                elif item["orderFlavorCoverage"] != None and item["orderFlavorBizcocho"] != None:
                    order_item = OrderItem.objects.create(
                        product=Product.objects.get(id=item["product"]),
                        order=order, quantity=item["quantity"],
                        orderFlavorCoverage=FlavorCoverage.objects.get(
                            id=item["orderFlavorCoverage"]),
                        orderFlavorBizcocho=FlavorBizcocho.objects.get(
                            id=item["orderFlavorBizcocho"]),

                        validateOrderItem=True)
                    order_item.save()
                else:
                    order_item = OrderItem.objects.create(
                        product=Product.objects.get(id=item["product"]),
                        order=order, quantity=item["quantity"],
                        validateOrderItem=True)
                    order_item.save()
                    for grupoGalletitas in item['box_product']:
                        BoxProduct.objects.create(
                            order_item=order_item,
                            orderFlavor=Flavor.objects.get(
                                id=grupoGalletitas["orderFlavor"]),
                            quantity=grupoGalletitas["quantity"]
                        ).save()

                    print("a")
            ############################FIN########################################3#

        order.nombrePagadorFull = nombrePagador + " " + apellidoPagador
        if total == float(order.get_cart_total):
            if request.data["metodoPago"] == "tarjeta":
                # AQUI REALIZAR EL PAGO (MercadoPago)
                # cambiar aqui el sdk y tambien en el otro views (donde renderiza las vistas)
                # credencial prueba
                sdk = mercadopago.SDK(
                    os.getenv("MERCADOPAGO_ACCESS_TOKEN_PRUEBA"))

                # Produccion cuenta
                # sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN_PRODUCCION"))
                preference_data = {
                    "items": [
                        {
                            "title": "Productos Varios",
                            "currency_id": "PEN",
                            "quantity": 1,
                            "unit_price": total
                        }
                    ],
                    # "payer": {
                    #    "name": nombrePagador,
                    #    "surname": apellidoPagador,
                    #    "identification": {
                    #        "type": "DNI",
                    #        "number": request.data["documentoDNI"]
                    #    },
                    # },
                    "back_urls": {
                        # "success": "https://kiomi-test-v1.herokuapp.com/payment/?dateDelivery="+str(dateDelivery)+"&identificador="+identificador,
                        # "failure": "https://kiomi-test-v1.herokuapp.com/payment/",
                        # "pending": "https://kiomi-test-v1.herokuapp.com/payment/?dateDelivery="+str(dateDelivery)+"&identificador="+identificador
                        # solo envia la fecha si la compra es exitosa (o pendiente)
                        "success": "http://127.0.0.1:8000/payment/?dateDelivery="+str(dateDelivery)+"&identificador="+identificador,
                        "failure": "http://127.0.0.1:8000/payment/",
                        "pending": "http://127.0.0.1:8000/payment/?dateDelivery="+str(dateDelivery)+"&identificador="+identificador,
                    },
                    "auto_return": "approved",
                    "payment_methods": {
                        "excluded_payment_types": [
                            {
                                "id": "atm"
                            }
                        ],
                        "installments": 1
                    },
                    # "notification_url": "http://localhost:8000/api/payment-status/",
                    "notification_url": "https://enyd3sjcyxeoada.m.pipedream.net",

                    "external_reference": order.orderUniqueIdentifier,

                    "statement_descriptor": "PasteleriaKIOMI",

                    # hacer un request aqui:
                    # https://api.mercadopago.com/v1/payments/1244089634?access_token=TEST-3835660200770784-112403-16b20a3f29a10626c6224c4ce9886139-230307119

                }

                preference_response = sdk.preference().create(preference_data)
                preference = preference_response["response"]

                print(preference)

                #### OJO: ESTA PARTE ES IMPORTANTE####
                # el metodoPago se usa como validacion en la vista de PaymentsViews (ver products/views.py)
                # si no se tiene metodo de pago es que no se paso por esta vista
                order.metodoPago = "tarjeta"
            if request.data["metodoPago"] == "yape":
                order.metodoPago = "yape"
                preference = {"message": "se pago con yape!"}
                print("yape")
            if request.data["metodoPago"] == "plin":
                order.metodoPago = "plin"
                preference = {"message": "se pago con plin!"}
                print("plin")
        else:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

        order.save()

        print('yep total: ', total)

        # fin del if
        return Response(preference, status=status.HTTP_200_OK)


class CustomerViewSet(
    viewsets.GenericViewSet
):
    """
    Lista de items que el cliente añadió a su carrito (usar para POST, UPDATE y DELETE)
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # def list(self, request, *args, **kwargs):
    #  queryset = self.filter_queryset(self.get_queryset())
    #  serializer = self.get_serializer(queryset, many=True)
    #  return Response(serializer.data)

    def list(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            instance = request.user.customer
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ValidateShipping(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        updated_values = {
            'nombrePersonaEnvio': request.data["nombrePersonaEnvio"],
            'address': request.data["address"],
            'distrito': request.data["distrito"],
            'phoneNumber': request.data["phoneNumber"],
            'reference': request.data["reference"]}

        if request.user.is_authenticated:
            print("request", request.data)
            customer = request.user.customer
            order = Order.objects.get(customer=customer, complete=0)
            # save shippingaddress information

            ShippingAddress.objects.update_or_create(
                customer=customer, order=order,
                defaults=updated_values)
            return Response({"shipping_saved": True}, status=status.HTTP_200_OK)
        else:  # si no se esta loggeado
            # Este es el momento cuando se crea el order
            # request.data["identificador"] solo es "" cuando no hay un order creado, una vez
            # se crea un order la primera vez, tendra un valor.
            if request.data["identificador"] == "":
                order = Order.objects.create(complete=0)
            else:
                order = Order.objects.get(
                    complete=0, orderUniqueIdentifier=request.data["identificador"])

            ShippingAddress.objects.update_or_create(order=order,
                                                     defaults=updated_values)

            return Response({"orderUniqueIdentifier": order.orderUniqueIdentifier}, status=status.HTTP_200_OK)


class DatePicker(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # Revisar esto.
        print(request.user)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=0)
            total_items_calendar = order.get_cart_items
        else:  # Si no se esta loggeado se obtendra el total_items_calendar de los cookies
            cookies_cart = json.loads(request.COOKIES['cart'])
            total_items_calendar = sum(item['quantity']
                                       for item in cookies_cart)
        invalid_dates, disabled_sundays, to_date, from_date = OrderServices.disabled_dates(
            total_items_calendar)
        responses = {
            "invalid_dates": invalid_dates,
            "disabled_sundays": disabled_sundays,
            "to_date": to_date,
            "from_date": from_date
        }
        return Response(responses, status=status.HTTP_200_OK)
