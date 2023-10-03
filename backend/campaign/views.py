import datetime
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CampaignForm, CampaignSMSForm, CampaignEmailForm, CampaignAudioForm, CampaignDisapproveForm
from .models import CampaignZip, Campaign, CampaignEmailType, CampaignAudio, CampaignSMS, CampaignEmail, \
    CampaignEmailTemplate
from core.utils import fancy_message, is_admin, string_to_context
from django.core.paginator import Paginator
from django.conf import settings as django_settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse


@login_required(login_url="/")
def CampaignResubmit(request, pk, *args, **kwargs):
    campaign = get_object_or_404(Campaign, id=pk, status="disapproved", customer=request.user)
    campaign_sms = CampaignSMS.objects.get(campaign_id=campaign.id)
    campaign_email = CampaignEmail.objects.get(campaign_id=campaign.id)
    campaign_audio = CampaignAudio.objects.get(campaign_id=campaign.id)
    campaign_sms_data = {}
    campaign_email_data = {}
    if request.method == "POST":
        selected_template = request.POST.get("selected-template", None)
        campaign_sms_data = {
            "type": request.POST.getlist("type")[0],
            "body": request.POST.getlist("body")[0]
        }
        campaign_email_data = {
            "type": request.POST.getlist("type")[1],
            "subject": request.POST.get("subject"),
            "body": request.POST.getlist("body")[1]
        }
        if selected_template:
            form2 = CampaignSMSForm(instance=campaign_sms, data=campaign_sms_data)
            if form2.is_valid():
                form3 = CampaignEmailForm(instance=campaign_email, data=campaign_email_data)
                if form3.is_valid():
                    form4 = CampaignAudioForm(instance=campaign_audio, data=request.POST, files=request.FILES)
                    if form4.is_valid():
                        campaign.email_template = CampaignEmailTemplate.objects.get(id=selected_template)
                        campaign.save()
                        form2.save()
                        form3.save()

                        form4_obj = form4.save()
                        if form4_obj.file and form4_obj.text:
                            form4_obj.text = ""
                        form4_obj.save()
                        campaign.save()
                        fancy_message(request, "Campaign information resubmitted", level="success")
                        return redirect(f"campaign:dashboard")
                    else:
                        fancy_message(request, form4.errors, level="error")
                else:
                    fancy_message(request, form3.errors, level="error")
            else:
                fancy_message(request, form2.errors, level="error")
        else:
            fancy_message(request, "please select an email template", level="error")
    form2 = CampaignSMSForm(instance=campaign_sms, initial=campaign_sms_data)
    form3 = CampaignEmailForm(instance=campaign_email, initial=campaign_email_data)
    form4 = CampaignAudioForm(instance=campaign_audio, initial=request.FILES)
    email_templates = CampaignEmailTemplate.objects.filter(is_active=True)
    my_context = {
        "Title": f"campaign | {pk}",
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "campaign": campaign,
        "templates": email_templates,
        "audio_instance": campaign_audio.file,
    }
    return render(request, "dashboard/campaign_resubmit.html", my_context)


# Create your views here.
@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
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
            return redirect("campaign:adminCampaigns")
        else:
            fancy_message(request, form.errors, level="error")
            return redirect("campaign:adminCampaigns")
    else:
        fancy_message(request, "invalid method", level="error")
        return redirect("campaign:adminCampaigns")


@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def AdminCampaignAudio(request, *args, **kwargs):
    if request.method == "POST":
        queryset = get_object_or_404(CampaignAudio, id=request.POST.get("change-audio-campaign-id", 0))
        form = CampaignAudioForm(instance=queryset, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.text = ""
            obj.save()
            fancy_message(request, f"Campaign-{obj.id} : audio file updated", level="success")
            return redirect("campaign:adminCampaigns")
        else:
            fancy_message(request, form.errors, level="error")
            return redirect("campaign:adminCampaigns")
    else:
        fancy_message(request, "invalid method", level="error")
        return redirect("campaign:adminCampaigns")


# Create your views here.
@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def AdminCampaignActions(request, id, status, *args, **kwargs):
    queryset = Campaign.objects.get(pk=id)
    queryset.status = str(status)
    queryset.admin = request.user
    if status == "processing":
        queryset.is_resubmit = False
    queryset.save()
    fancy_message(request, f"Campaign-{id} : status changed to {status}", level="success")
    return redirect("campaign:adminCampaigns")


@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
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


@login_required(login_url="/")
def Dashboard(request, *args, **kwargs):
    payment = request.GET.get("payment_success", None)
    if payment and payment == "true":
        fancy_message(request, "Your Payment was successful and after review your campaign will start", level="success")
    elif payment and payment == "false":
        fancy_message(request, "Payment failed", level="error")
    queryset = Campaign.objects.filter(customer=request.user)
    pagination = Paginator(queryset, per_page=10)
    page = request.GET.get('page', 1)
    items = pagination.get_page(page)
    my_context = {
        "Title": f"Dashboard",
        "campaigns": items,
        "today": datetime.datetime.now(),
        "base_url": django_settings.EXTERNAL_API_BASE_URL,
    }
    return render(request, "dashboard/dashboard.html", my_context)


def ListOfEmailTemplates(request, *args, **kwargs):
    queryset = CampaignEmailTemplate.objects.filter(is_active=True)
    serializer = [
        {
            "id": item.id,
            "template": item.template.url,
            "image": item.thumbnail.url,
        }
        for item in queryset
    ]

    return JsonResponse(serializer, safe=False)


@csrf_exempt
def EmailPreview(request, pk, *args, **kwargs):
    if request.method == "POST":
        queryset = get_object_or_404(CampaignEmailTemplate, id=pk)
        content = request.POST.get("content", None)
        my_context = {
            "content": queryset.get_rendered_content({"body": content})
        }
        return HttpResponse(my_context.get("content"), status=200)
    else:
        return HttpResponse("get not allowed", status=400)


@login_required(login_url="/")
def CampaignCreate(request, *args, **kwargs):
    campaign_data = {}
    campaign_sms_data = {}
    campaign_email_data = {}
    if request.method == "POST":
        campaign_data = {
            "type": request.POST.getlist("type")[0],
        }
        selected_template = request.POST.get("selected-template", None)
        campaign_sms_data = {
            "type": request.POST.getlist("type")[1],
            "body": request.POST.getlist("body")[0]
        }
        campaign_email_data = {
            "type": request.POST.getlist("type")[2],
            "subject": request.POST.get("subject"),
            "body": request.POST.getlist("body")[1]
        }
        zip_selects = [request.POST.get("select-1"), request.POST.get("select-2"), request.POST.get("select-3")]
        form1 = CampaignForm(campaign_data)
        if selected_template:
            if form1.is_valid():
                form2 = CampaignSMSForm(campaign_sms_data)
                if form2.is_valid():
                    form3 = CampaignEmailForm(campaign_email_data)
                    if form3.is_valid():
                        form4 = CampaignAudioForm(request.POST, files=request.FILES)
                        if form4.is_valid():
                            campaign_obj = form1.save(commit=False)
                            campaign_obj.customer = request.user
                            campaign_obj.email_template = CampaignEmailTemplate.objects.get(id=selected_template)
                            campaign_obj.save()
                            campaign_obj.zips.set(zip_selects)
                            sms_obj = form2.save(commit=False)
                            sms_obj.campaign = campaign_obj
                            sms_obj.save()
                            email_obj = form3.save(commit=False)
                            email_obj.campaign = campaign_obj
                            email_obj.save()
                            audio_obj = form4.save(commit=False)
                            audio_obj.campaign = campaign_obj
                            audio_obj.save()
                            fancy_message(request, "New campaign successfully created", level="success")
                            if request.POST["payment_method"] == "pay":
                                return redirect(f"/checkout/payment/{campaign_obj.id}/")
                            else:
                                return redirect(f"campaign:dashboard")
                        else:
                            fancy_message(request, form4.errors, level="error")
                    else:
                        fancy_message(request, form3.errors, level="error")
                else:
                    fancy_message(request, form2.errors, level="error")
            else:
                fancy_message(request, form1.errors, level="error")
        else:
            fancy_message(request, "please select an email template", level="error")
    form1 = CampaignForm(initial=campaign_data)
    form2 = CampaignSMSForm(initial=campaign_sms_data)
    form3 = CampaignEmailForm(initial=campaign_email_data)
    form4 = CampaignAudioForm(request.FILES)
    zips = CampaignZip.objects.filter(is_active=True)
    email_templates = CampaignEmailTemplate.objects.filter(is_active=True)
    my_context = {
        "Title": f"Campaign | Create",
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "zips": zips,
        "templates": email_templates,
    }
    return render(request, "dashboard/create_campaign.html", my_context)
