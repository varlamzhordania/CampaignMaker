from django.urls import path
from .views import Profile, Logout, Login, Register, ChangePassword

app_name = 'account'

urlpatterns = [
    path("", Login, name="login"),
    path("logout/", Logout, name="logout"),
    path("register/", Register, name="register"),
    path("change_password/", ChangePassword, name="changePassword"),
    path("profile/", Profile, name="profile"),
]
