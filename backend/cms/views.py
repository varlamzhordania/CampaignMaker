from django.shortcuts import render, get_object_or_404
from core.utils import fancy_message, is_admin, string_to_context
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required, user_passes_test
from campaign.forms import CampaignForm, CampaignSMSForm, CampaignEmailForm, CampaignAudioForm, CampaignDisapproveForm
from campaign.models import CampaignZip, Campaign, CampaignEmailType, CampaignAudio, CampaignSMS, CampaignEmail, \
    CampaignEmailTemplate, CampaignType
from main.models import Ticket, TicketAttachment, ContactUs
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from main.forms import TicketCommentCreateForm, TicketAttachmentForm


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminTicketAction(request, pk, status, *args, **kwargs):
    queryset = get_object_or_404(Ticket, id=pk)
    queryset.status = status
    queryset.save()
    fancy_message(
        request,
        f"Ticket-{pk} : status successfully changed to {status}",
        level="success"
    )
    return redirect("cms:adminTicketRetrieve", pk=pk)


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminTicketRetrieve(request, pk, *args, **kwargs):
    queryset = get_object_or_404(Ticket, pk=pk)
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
            return redirect("cms:adminTicketRetrieve", pk=queryset.id)
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
    return render(request, "dashboard/admin/ticket_retrieve.html", my_context)


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminTicketList(request, *args, **kwargs):
    status = request.GET.get("status", None)
    page = request.GET.get("page", 1)
    queryset = Ticket.objects.all()

    if status:
        queryset = queryset.filter(status=status)

    paginator = Paginator(queryset, per_page=10)
    items = paginator.get_page(page)

    my_context = {
        "Title": "Ticket List",
        "tickets": items,
        "status": status
    }

    return render(request, "dashboard/admin/ticket_list.html", my_context)


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminContactList(request, *args, **kwargs):
    check = bool(request.GET.get("is_check", False))
    page = request.GET.get("page", 1)
    queryset = ContactUs.objects.all()

    if check:
        queryset = queryset.filter(is_check=True)

    paginator = Paginator(queryset, per_page=10)
    items = paginator.get_page(page)

    my_context = {
        "Title": "Contact List",
        "contacts": items,
        "is_check": check,
    }

    return render(request, "dashboard/admin/contact_list.html", my_context)


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminContactAction(request, pk, check):
    queryset = get_object_or_404(ContactUs, id=pk)
    if check == "true":
        queryset.is_check = True
        queryset.save()
        fancy_message(
            request,
            f"Contact-{pk} : check status successfully changed",
            level="success"
        )
        return redirect("cms:adminContacts")
    elif check == "false":
        queryset.is_check = False
        queryset.save()
        fancy_message(
            request,
            f"Contact-{pk} : check status successfully changed",
            level="success"
        )
        return redirect("cms:adminContacts")
    else:
        fancy_message(
            request,
            f"incorrect query param",
            level="error"
        )
        return redirect("cms:adminContacts")


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminCampaignList(request, *args, **kwargs):
    form = CampaignDisapproveForm()
    form2 = CampaignAudioForm()
    status = request.GET.get("status", None)
    search = request.GET.get("search", None)
    resubmit = request.GET.get("resubmit", None)
    page = request.GET.get('page', 1)
    queryset = Campaign.objects.all()

    if status:
        queryset = queryset.filter(status=status)

    if search:
        queryset = queryset.filter(
            Q(id__icontains=search) |
            Q(customer__username=search) |
            Q(customer__email__icontains=search)
        )

    if resubmit:
        queryset = queryset.filter(is_resubmit=resubmit)
    pagination = Paginator(queryset, per_page=10)
    items = pagination.get_page(page)
    my_context = {"Title": "Campaign List", "campaigns": items, "form": form, "form2": form2, "status": status,
                  "is_resubmit": resubmit}
    return render(request, "dashboard/admin/campaign_list.html", my_context)


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminCampaignNote(request, *args, **kwargs):
    if request.method == "POST":
        queryset = get_object_or_404(Campaign, id=request.POST.get("disapprove-campaign-id", 0))
        data = {
            "admin": request.user,
            "note": request.POST.get("note", ""),
            "status": "disapproved",
        }
        form = CampaignDisapproveForm(instance=queryset, data=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_resubmit = False
            obj.save()
            fancy_message(request, f"Campaign-{obj.id} : status changed to {data.get('status')}", level="success")
            return redirect("cms:adminCampaigns")
        else:
            fancy_message(request, form.errors, level="error")
            return redirect("cms:adminCampaigns")
    else:
        fancy_message(request, "invalid method", level="error")
        return redirect("cms:adminCampaigns")


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminCampaignAudio(request, *args, **kwargs):
    if request.method == "POST":
        queryset = get_object_or_404(CampaignAudio, campaign_id=request.POST.get("change-audio-campaign-id", 0))
        data = {
            "text": queryset.text
        }
        form = CampaignAudioForm(instance=queryset, data=data, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            fancy_message(request, f"Campaign-{obj.id} : audio file updated", level="success")
            return redirect("cms:adminCampaigns")
        else:
            fancy_message(request, form.errors, level="error")
            return redirect("cms:adminCampaigns")
    else:
        fancy_message(request, "invalid method", level="error")
        return redirect("cms:adminCampaigns")


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def AdminCampaignActions(request, id, status, *args, **kwargs):
    queryset = Campaign.objects.get(pk=id)
    queryset.status = str(status)
    queryset.admin = request.user
    if status == "processing":
        queryset.is_resubmit = False
        # call_api(queryset)
    queryset.save()
    fancy_message(request, f"Campaign-{id} : status changed to {status}", level="success")
    return redirect("cms:adminCampaigns")


# HTTP API

@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def ListOfCampaigns(request, *args, **kwargs):
    queryset = Campaign.objects.all()
    params = request.GET.get("id", None)
    if params:
        queryset = queryset.filter(id=params)
    serializer = [
        {
            "id": item.id,
            "customer": item.customer.username,
            "type": {
                "id": item.type.id,
                "name": item.type.name,
                "slug": item.type.slug,
                "price": item.type.price,
            },
            "email": {
                "id": item.campaign_email.id,
                "subject": item.campaign_email.subject,
                "body": item.campaign_email.body,

            },
            "sms": {
                "id": item.campaign_sms.id,
                "body": item.campaign_sms.body,
            },
            "audio": {
                "id": item.campaign_audio.id,
                "text": item.campaign_audio.text,
            }
        }
        for item in queryset
    ]

    return JsonResponse(serializer, safe=False)
