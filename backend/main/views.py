from django.shortcuts import render, get_object_or_404
from .models import CustomerVideo, FAQ, Categories, Page


# Create your views here.

def home(request, *args, **kwargs):
    video_queryset = CustomerVideo.objects.filter(is_active=True)
    faq_queryset = FAQ.objects.filter(is_active=True)
    page = Page.objects.filter(type="home").first()
    my_context = {
        "Title": "Home",
        "customer_videos": video_queryset,
        "FAQ": faq_queryset,
        "page": page
    }
    return render(request, "main/home.html", my_context)


def category(request, slug, *args, **kwargs):
    queryset = get_object_or_404(Categories, slug=slug, is_active=True)
    my_context = {
        "category": queryset,
        "page": queryset.category_page
    }
    return render(request, "main/category_obj.html", my_context)


def contact_us(request, *args, **kwargs):
    page = Page.objects.filter(type="contact").first()
    my_context = {
        "Title": "Contact us",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def about_us(request, *args, **kwargs):
    page = Page.objects.filter(type="about").first()
    my_context = {
        "Title": "About us",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def privacy_policy(request, *args, **kwargs):
    page = Page.objects.filter(type="privacy").first()
    my_context = {
        "Title": "Privacy Policy",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def terms(request, *args, **kwargs):
    page = Page.objects.filter(type="terms").first()
    my_context = {
        "Title": "Terms",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def refund(request, *args, **kwargs):
    page = Page.objects.filter(type="refund").first()
    my_context = {
        "Title": "Refund",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def feedback(request, *args, **kwargs):
    page = Page.objects.filter(type="feedback").first()
    my_context = {
        "Title": "Feedback",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)
