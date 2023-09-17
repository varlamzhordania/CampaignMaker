from django.urls import path
from .views import Login, Register, AdminLogin

app_name = 'campaign'

urlpatterns = [
    path("", Login, name="login"),
    path("admin_login/", AdminLogin, name="admin_login"),
    path("register/", Register, name="register"),
]
