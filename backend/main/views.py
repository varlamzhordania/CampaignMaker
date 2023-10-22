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
