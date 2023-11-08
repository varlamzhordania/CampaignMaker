from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomerVideo, FAQ, Categories, Page, Ticket, TicketAttachment
from django.core.paginator import Paginator
from .forms import TicketCreateForm, TicketAttachmentForm, TicketCommentCreateForm
from core.utils import fancy_message
from django.core.cache import cache


# Create your views here.

def ticket_retrieve(request, pk, *args, **kwargs):
    queryset = get_object_or_404(Ticket, pk=pk, author=request.user)
    if request.method == "POST":
        form = TicketCommentCreateForm(request.POST)
        formset = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.ticket = queryset
            comment.save()

            for file in request.FILES.getlist('file'):
                TicketAttachment.objects.create(file=file, ticket=queryset, comment=comment)

            fancy_message(
                request,
                "Your comment added to the ticket",
                level="success"
            )
            return redirect("main:ticketRetrieve", pk=queryset.id)
        else:
            fancy_message(request, formset.errors, level="error")
            fancy_message(request, form.errors, level="error")
    else:
        form = TicketCommentCreateForm(initial=request.POST)
        formset = TicketAttachmentForm()
    my_context = {
        "Title": f"Ticket-{pk}",
        "ticket": queryset,
        "form": form,
        "formset": formset,

    }
    return render(request, "dashboard/ticket_retrieve.html", my_context)


def ticket_create(request, *args, **kwargs):
    if request.method == "POST":
        form = TicketCreateForm(request.POST)
        formset = TicketAttachmentForm(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()

            for file in request.FILES.getlist('file'):
                TicketAttachment.objects.create(file=file, ticket=ticket)

            fancy_message(
                request,
                "Our support will review and answer you as soon as possible",
                level="success"
            )
            return redirect("main:ticketList")
        else:
            fancy_message(request, formset.errors, level="error")
            fancy_message(request, form.errors, level="error")
    else:
        form = TicketCreateForm(initial=request.POST)
        formset = TicketAttachmentForm()

    context = {
        "Title": "Create New Ticket",
        "form": form,
        "formset": formset,
    }

    return render(request, "dashboard/ticket_create.html", context)


def ticket_list(request, *args, **kwargs):
    queryset = Ticket.objects.filter(author=request.user)
    pagination = Paginator(queryset, per_page=10)
    page = request.GET.get('page', 1)
    items = pagination.get_page(page)
    my_context = {
        "Title": "Ticket List",
        "tickets": items
    }
    return render(request, "dashboard/ticket_list.html", my_context)


def home(request, *args, **kwargs):
    page_data = cache.get("home_page")
    customer_videos_data = cache.get("customer_videos")
    faq_data = cache.get("faq")

    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="home").first()
        cache.set('home_page', page, 900)

    if customer_videos_data is not None:
        video_queryset = customer_videos_data
    else:
        video_queryset = CustomerVideo.objects.filter(is_active=True)
        cache.set('customer_videos', video_queryset, 900)

    if faq_data is not None:
        faq_queryset = faq_data
    else:
        faq_queryset = FAQ.objects.filter(is_active=True)
        cache.set('faq', faq_queryset, 900)

    my_context = {
        "Title": "Home",
        "customer_videos": video_queryset,
        "FAQ": faq_queryset,
        "page": page
    }
    return render(request, "main/home.html", my_context)


def category(request, slug, *args, **kwargs):

    queryset_data = cache.get(f"category-{slug}")
    if queryset_data is not None:
        queryset = queryset_data
    else:
        queryset = get_object_or_404(Categories, slug=slug, is_active=True)
        cache.set(f"category-{slug}", queryset, 900)

    my_context = {
        "category": queryset,
        "page": queryset.category_page
    }
    return render(request, "main/category_obj.html", my_context)


def contact_us(request, *args, **kwargs):
    page_data = cache.get("contact_page")
    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="contact").first()
        cache.set('contact_page', page, 900)

    my_context = {
        "Title": "Contact us",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def about_us(request, *args, **kwargs):
    page_data = cache.get("about_page")
    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="about").first()
        cache.set('about_page', page, 900)

    my_context = {
        "Title": "About us",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def privacy_policy(request, *args, **kwargs):
    page_data = cache.get("privacy_page")
    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="privacy").first()
        cache.set('privacy_page', page, 900)

    my_context = {
        "Title": "Privacy Policy",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def terms(request, *args, **kwargs):
    page_data = cache.get("term_page")
    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="terms").first()
        cache.set('term_page', page, 900)

    my_context = {
        "Title": "Terms",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def refund(request, *args, **kwargs):
    page_data = cache.get("refund_page")
    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="refund").first()
        cache.set('refund_page', page, 900)

    my_context = {
        "Title": "Refund",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)


def feedback(request, *args, **kwargs):
    page_data = cache.get("feedback_page")
    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type="feedback").first()
        cache.set('feedback_page', page, 900)

    my_context = {
        "Title": "Feedback",
        "page": page
    }
    return render(request, "main/dynamic_object.html", my_context)
