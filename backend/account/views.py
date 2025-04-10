from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from core.utils import fancy_message
from main.models import Page

from .decorators import unauthenticated_user
from .forms import StylesCustomUserCreationForm, StylesCustomUserChangeForm, \
    StylesCustomPasswordChangeForm
from .models import UserBusinessProfile


@login_required(login_url="/login")
def Profile(request, *args, **kwargs):
    user = request.user
    if request.method == "POST":
        form = StylesCustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            fancy_message(request, f"Profile updated successfully")
            return redirect("account:profile")
        else:
            fancy_message(request, form.errors, level="error")
            return redirect(request.META["HTTP_REFERER"])
    form = StylesCustomUserChangeForm(instance=user)
    password_form = StylesCustomPasswordChangeForm(user)
    my_context = {"Title": f"Profile | {request.user}", "form": form,
                  "password_form": password_form}
    return render(request, "dashboard/profile.html", my_context)


@login_required(login_url="/login")
def ChangePassword(request, *args, **kwargs):
    if request.method == "POST":
        form = StylesCustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            fancy_message(request, f"Your password was successfully updated!")
            return redirect("account:profile")
        else:
            fancy_message(request, form.errors, level="error")
            return redirect(request.META["HTTP_REFERER"])
    raise Http404("page not found")


@unauthenticated_user
def Login(request, *args, **kwargs):
    if request.method == "POST":
        email_data = request.POST.get("email")
        password_data = request.POST.get("password")
        if email_data and password_data:
            user = authenticate(request, email=email_data, password=password_data)
            if user:
                login(request, user)
                fancy_message(request, f"welcome {user.username}")
                return redirect("campaign:dashboard")
            else:
                fancy_message(request, "Email or Password is incorrect", level="error")
                return redirect(request.META["HTTP_REFERER"])
        else:
            fancy_message(request, "Email and Password is required", level="error")
            return redirect(request.META["HTTP_REFERER"])
    page = Page.objects.filter(type="signIn").first()
    my_context = {
        "Title": "Login",
        "page": page,
    }
    return render(request, "login.html", my_context)


@login_required(login_url="/login")
def Logout(request, *args, **kwargs):
    logout(request)
    fancy_message(request, "Logout successful")
    return redirect("account:login")


@unauthenticated_user
def Register(request, *args, **kwargs):
    if request.method == "POST":
        form = StylesCustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            fancy_message(request, f"welcome {user.username}")
            return redirect("account:businessSetup")
        else:
            fancy_message(request, form.errors, level="error")

    previous_data = {
        "first_name": request.POST.get("first_name", None),
        "middle_name": request.POST.get("middle_name", None),
        "last_name": request.POST.get("last_name", None),
        "email": request.POST.get("email", None),
        "username": request.POST.get("username", None),
        "phone_number": request.POST.get("phone_number", None),
    }
    form = StylesCustomUserCreationForm(initial=previous_data)
    my_context = {"Title": "Register", "form": form}
    return render(request, "register.html", my_context)


@login_required(login_url="/login")
def BusinesSetup(request, *args, **kwargs):
    user = request.user

    if not user.show_questions:
        return redirect("campaign:dashboard")

    user_profile, created = UserBusinessProfile.objects.get_or_create(user=user)

    profile_progress = user_profile.get_profile_progress()
    incomplete_steps = profile_progress["remaining_steps"]

    my_context = {
        "Title": "Tell us about your business",
        "incomplete_steps": incomplete_steps,
    }

    return render(request, "dashboard/business_setup.html", my_context)
