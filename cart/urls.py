from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name="cart"),
    path("payment/", views.order_payment, name="payment"),
    path("cancelled/", views.cancelled, name="cancelled"),
    path("handler/", views.order_payment, name="handler"),
    path("callback/", views.callback, name="callback"),
]
