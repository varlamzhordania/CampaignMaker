from django.urls import path
from .views import Checkout,my_webhook_view

app_name = 'checkout'

urlpatterns = [
    path("payment/<int:pk>/", Checkout, name="checkout"),
    path("webhook/", my_webhook_view, name="webhook"),
]
