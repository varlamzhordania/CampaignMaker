from django.shortcuts import render


# Create your views here.

def Login(request, *args, **kwargs):
    my_context = {"Title": "Login"}
    return render(request, "login.html", my_context)


def AdminLogin(request, *args, **kwargs):
    my_context = {"Title": "Admin Login"}
    return render(request, "admin_login.html", my_context)


def Register(request, *args, **kwargs):
    my_context = {"Title": "Register"}
    return render(request, "register.html", my_context)
