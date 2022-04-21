from datetime import datetime
from django.shortcuts import render

from django.views import View
from products.models import Customer

from products.models import Order

#from django.contrib.auth.models import User
# import login register tools
#from django.contrib import messages
#from .form import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import HttpResponseRedirect
# Create your views here.
import mercadopago
# imports para envio correo
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from api.serializer.checkout_serializers import CheckoutSerializer

from dotenv import load_dotenv
import os
load_dotenv()

#########################


class StoreView(View):
    def get(self, request):
        # validate products
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
            items = order.orderitem_set.filter(validateOrderItem=False)
            print("itemsss", items)
            items.delete()
        return render(request, 'products/store.html')


class ProductDetailsView(View):
    def get(self, request):
        return render(request, 'products/productDetails.html')


class CarView(View):
    def get(self, request):
        # validate products
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
            items = order.orderitem_set.filter(validateOrderItem=False)
            print("itemsss", items)
            items.delete()
        return render(request, 'products/car.html')


class AboutView(View):
    def get(self, request):
        # validate products
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
            items = order.orderitem_set.filter(validateOrderItem=False)
            print("itemsss", items)
            items.delete()
        return render(request, 'products/about.html')


class HomeView(View):
    def get(self, request):
        if(not (hasattr(request.user, 'customer')) and request.user.is_authenticated):
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            user_id = request.user
            customer = Customer.objects.create(
                user=user_id,
                name=first_name,
                lastName=last_name,
                email=email
            )
            print("customer", customer)
        # validate products
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
            items = order.orderitem_set.filter(validateOrderItem=False)
            print("itemsss", items)
            items.delete()
        return render(request, 'products/home.html')


class CheckoutView(View):
    def get(self, request):
        # validate products
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
            items = order.orderitem_set.filter(validateOrderItem=False)
            print("itemsss", items)
            items.delete()
        return render(request, 'products/checkout.html')
# Crearemos las funciones de register login logout


class PaymentView(View):
    def enviarCorreo(self, request, order, listaItems, date_delivery, email_to_send):
        """Esta función solo funciona con un order que tenga los metodos "getcartTotal y 
        los atributos orderUniqueIdentifier y shippingAddress propios de un order que 
        proviene de la vista de checkout de este proyecto """
        template = render_to_string('confirmation-email/template.html',
                                    {"cartTotal": order.get_cart_total, "items": listaItems, "orderUniqueIdentifier": order.orderUniqueIdentifier, "shippingAdress": order.shippingAddress, "dateDelivery": date_delivery})
        email = EmailMessage(
            'Gracias por comprar en Kiomi Store!!!',
            template,
            os.getenv("EMAIL_HOST_USER"),
            [email_to_send],
        )
        # email.fail_silently = False
        email.content_subtype = "html"
        email.send(fail_silently=False)

    def get(self, request):

        # cambiar aqui el sdk y tambien en el otro views (api)
        # credencial prueba
        sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN_PRUEBA"))
        # Produccion
        # sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN_PRODUCCION"))

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=0
            )
            items = order.orderitem_set.all()
            serializer = CheckoutSerializer(items, many=True)

            requestURL = request.GET.get('status', '')
            # get la fecha y convcertirla de num enteros a tipo fecha
            date_delivery = datetime.fromtimestamp(
                int(request.GET.get('dateDelivery', ''))/1000.0).date()
            # NOTA: Esta fecha esta en UTC-5 (hora peru) en el server local, revisar si es asi tambien en el server de producción
            if order.metodoPago is not None:
                # Se hara lo siguiente si el pedido esta pendiente de confirmación
                if requestURL == "pending":
                    self.enviarCorreo(request, order, serializer.data,
                                      date_delivery, request.user.email)

                    # Se pone el pedido en estado pendiente de confirmacion y se postea la fecha del delibery
                    order.complete = 3
                    order.date_delivery = date_delivery
                    order.save()
                    # si no hay errores en este if, el flujo para pendiente termina aqui
                    return render(request, 'payments/payment.html')

                # Se hace esto cuando el pago no es pendiente pero se presiono el boton de confirmar pago:
                # INICIO
                filters = {"external_reference": order.orderUniqueIdentifier}
                search_payment_response = sdk.payment().search(filters)
                search_payment = search_payment_response["response"]["results"]
                # print(preference_response["response"]["results"]["status"])

                print("........")
                if len(search_payment) != 0:
                    print("estatus", search_payment[0]["status"])
                    print("-")
                    print("payment_results", search_payment[0])
                    if search_payment[0]["status"] == "approved":

                        # Aqui se enviara un correo de la confirmación del pedido
                        self.enviarCorreo(request, order, serializer.data,
                                          date_delivery, request.user.email)
                        # Se completara el pedido y se postea la fecha del delibery
                        order.complete = 1
                        order.date_delivery = date_delivery
                        order.save()
                    # FIN
        else:
            # ESTA PARTE CORRESPONDE A USUARIOS NO LOGGEADOS
            identificador = request.GET.get('identificador', '')

            try:
                order = Order.objects.get(
                    complete=0, orderUniqueIdentifier=identificador)
            except Order.DoesNotExist:
                return render(request, 'payments/payment.html')

            items = order.orderitem_set.all()
            serializer = CheckoutSerializer(items, many=True)

            email = request.COOKIES["email"]
            requestURL = request.GET.get('status', '')
            # get la fecha y convcertirla de num enteros a tipo fecha
            date_delivery = datetime.fromtimestamp(
                int(request.GET.get('dateDelivery', ''))/1000.0).date()
            # NOTA: Esta fecha esta en UTC-5 (hora peru) en el server local, revisar si es asi tambien en el server de producción
            if order.metodoPago is not None:
                # Se hara lo siguiente si el pedido esta pendiente de confirmación
                if requestURL == "pending":
                    self.enviarCorreo(request, order, serializer.data,
                                      date_delivery, email)

                    # Se pone el pedido en estado pendiente de confirmacion y se postea la fecha del delibery
                    order.complete = 3
                    order.date_delivery = date_delivery
                    order.save()
                    # Aqui se limpia las cookies
                    response = render(
                        request, 'payments/payment.html', {"email": email})
                    response.delete_cookie("email")
                    response.delete_cookie("cart")
                    # si no hay errores en este if, el flujo para pendiente termina aqui
                    return response

                # Se hace esto cuando el pago no es pendiente pero se presiono el boton de confirmar pago:
                # INICIO
                filters = {"external_reference": order.orderUniqueIdentifier}
                search_payment_response = sdk.payment().search(filters)
                search_payment = search_payment_response["response"]["results"]
                # print(preference_response["response"]["results"]["status"])

                print("........")
                if len(search_payment) != 0:
                    print("estatus", search_payment[0]["status"])
                    print("-")
                    print("payment_results", search_payment[0])
                    if search_payment[0]["status"] == "approved":

                        # Aqui se enviara un correo de la confirmación del pedido
                        self.enviarCorreo(
                            request, order, serializer.data, date_delivery, email)
                        # Se completara el pedido y se postea la fecha del delibery
                        order.complete = 1
                        order.date_delivery = date_delivery
                        order.save()

                        # Aqui se limpia las cookies
                        response = render(
                            request, 'payments/payment.html', {"email": email})
                        response.delete_cookie("email")
                        response.delete_cookie("cart")
                        return response
                    # FIN

        return render(request, 'payments/payment.html')

# class FailView(View):
#  def get(self, request):
#    return render(request, 'payments/fail.html')
# Crearemos las funciones de register login logout
#
#
# class PendingView(View):
#  def get(self, request):
#    return render(request, 'payments/pending.html')
# Crearemos las funciones de register login logout


# def welcome(request):
#   # return to cover page
#   return render(request, "login/")


class ProfileView(View):

    def get(self, request):
        # Hacer un redirect para evitar que un usuario no identificado pueda editar un perfil
        # PD. se uso mejor "LoginRequiredMixin"
        # if not request.user.is_authenticated:
        # return HttpResponseRedirect('/login/')
        return render(request, 'login/profile.html')


# def register(request):
#   # creamos un formulario de autentificacion vacio
#   form = UserRegisterForm()
#   if request.method == "POST":
#     # Añadimos los datos recibidos del formulario
#     form = UserRegisterForm(request.POST)
#     # Si el formulario es valido
#     if form.is_valid():
#       form.save()
#       # creamos una nueva cuenta de usuario
#       username = form.cleaned_data['username']
#       messages.success(request, f'usuario{username}creado')
#       return redirect('/')
#     else:
#       form = UserRegisterForm()
#   context = {'form': form}
#   return render(request, "login/register.html", context)
