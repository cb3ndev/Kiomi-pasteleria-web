from django.urls import path
from products.views import *
# Importar para login, logout, register, welcome
#from products.views import welcome, register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('store/', StoreView.as_view(), name="store"),
    path('product-details/', ProductDetailsView.as_view(), name="product-details"),
    path('car/', CarView.as_view(), name="car"),
    path('about/', AboutView.as_view(), name="about"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('payment/', PaymentView.as_view(), name="payment"),

    # path('welcome/', welcome, name="Welcome"),
    # path('register/', register, name="Register"),
    # path('login/', LoginView.as_view(template_name='login/login.html'), name="Login"),
    # path('logout/', LogoutView.as_view(template_name='login/logout.html'), name="Logout"),
    path('profile/', ProfileView.as_view(), name="Profile"),
]
