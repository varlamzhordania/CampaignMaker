from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CampaignForm, CampaignSMSForm, CampaignEmailForm, CampaignAudioForm
from .models import CampaignZip, Campaign
from core.utils import fancy_message, is_admin


# Create your views here.
@login_required(login_url="/")
@user_passes_test(is_admin)
def AdminCampaignActions(request, id, status, *args, **kwargs):
    queryset = Campaign.objects.get(pk=id)
    queryset.status = str(status)
    queryset.save()
    fancy_message(request, f"Campaign-{id} : status changed to {status}", level="success")
    return redirect("campaign:adminCampaigns")


@login_required(login_url="/")
@user_passes_test(is_admin)
def AdminCampaignList(request, *args, **kwargs):
    queryset = Campaign.objects.all().order_by("-id")
    my_context = {"Title": "Campaign List", "campaigns": queryset}
    return render(request, "dashboard/admin/campaign_list.html", my_context)


@login_required(login_url="/")
def Dashboard(request, *args, **kwargs):
    payment = request.GET.get("payment_success", None)
    campaign_data = {}
    campaign_sms_data = {}
    campaign_email_data = {}
    if payment and payment == "true":
        fancy_message(request, "Your Payment was successful and after review your campaign will start", level="success")
    elif payment and payment == "false":
        fancy_message(request, "Payment failed", level="error")
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
        "Title": f"Dashboard | {request.user.username}",
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "zips": zips
    }
    return render(request, "dashboard/dashboard.html", my_context)
