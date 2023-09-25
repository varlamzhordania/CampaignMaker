from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CampaignForm, CampaignSMSForm, CampaignEmailForm, CampaignAudioForm
from .models import CampaignZip, Campaign, CampaignEmailType
from core.utils import fancy_message, is_admin, string_to_context
from django.core.paginator import Paginator
from django.conf import settings as django_settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def AdminCampaignActions(request, id, status, *args, **kwargs):
    queryset = Campaign.objects.get(pk=id)
    queryset.status = str(status)
    queryset.admin = request.user
    queryset.save()
    fancy_message(request, f"Campaign-{id} : status changed to {status}", level="success")
    return redirect("campaign:adminCampaigns")


@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def AdminCampaignList(request, *args, **kwargs):
    queryset = Campaign.objects.all().order_by("-id")
    my_context = {"Title": "Campaign List", "campaigns": queryset}
    return render(request, "dashboard/admin/campaign_list.html", my_context)


@login_required(login_url="/")
def Dashboard(request, *args, **kwargs):
    payment = request.GET.get("payment_success", None)
    if payment and payment == "true":
        fancy_message(request, "Your Payment was successful and after review your campaign will start", level="success")
    elif payment and payment == "false":
        fancy_message(request, "Payment failed", level="error")
    queryset = Campaign.objects.filter(customer=request.user)
    pagination = Paginator(queryset, per_page=1)
    page = request.GET.get('page', 1)
    items = pagination.get_page(page)
    my_context = {
        "Title": f"Dashboard",
        "campaigns": items,
    }
    return render(request, "dashboard/dashboard.html", my_context)


@csrf_exempt
def EmailPreview(request, pk, *args, **kwargs):
    if request.method == "POST":
        queryset = get_object_or_404(CampaignEmailType, id=pk)
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
            "total": request.POST.get("total")
        }
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
        if form1.is_valid():
            form2 = CampaignSMSForm(campaign_sms_data)
            if form2.is_valid():
                form3 = CampaignEmailForm(campaign_email_data)
                if form3.is_valid():
                    form4 = CampaignAudioForm(request.POST, files=request.FILES)
                    if form4.is_valid():
                        campaign_obj = form1.save(commit=False)
                        campaign_obj.customer = request.user
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
                        return redirect(f"/checkout/payment/{campaign_obj.id}/")
                    else:
                        fancy_message(request, form4.errors, level="error")
                else:
                    fancy_message(request, form3.errors, level="error")
            else:
                fancy_message(request, form2.errors, level="error")
        else:
            fancy_message(request, form1.errors, level="error")
    form1 = CampaignForm(initial=campaign_data)
    form2 = CampaignSMSForm(initial=campaign_sms_data)
    form3 = CampaignEmailForm(initial=campaign_email_data)
    form4 = CampaignAudioForm(request.FILES)
    zips = CampaignZip.objects.filter(is_active=True)
    my_context = {
        "Title": f"Campaign | Create",
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "zips": zips
    }
    return render(request, "dashboard/create_campaign.html", my_context)


@login_required(login_url="/")
def CampaignRetrieve(request, pk, *args, **kwargs):
    queryset = get_object_or_404(Campaign, id=pk)
    my_context = {
        "Title": f"campaign | {pk}",
        "campaign": queryset
    }
    return render(request, "dashboard/campaign_retrieve.html", my_context)
