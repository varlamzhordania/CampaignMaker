import datetime
import logging

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings as django_settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction

from core.utils import fancy_message, is_admin
from main.models import Ticket

from .forms import (
    CampaignForm,
    CampaignSMSForm,
    CampaignEmailForm,
    CampaignAudioForm,
    CampaignSocialMediaEntryForm,
    CampaignSocialMediaFieldValueForm, CampaignSocialMediaUploadFileForm,
)

from .models import (
    CampaignZip,
    Campaign,
    CampaignEmailType,
    CampaignAudio,
    CampaignSMS,
    CampaignEmail,
    CampaignEmailTemplate,
    CampaignType,
    SocialMedia,
    CampaignSocialMediaEntry,
)

logger = logging.getLogger(__name__)


@login_required(login_url="/login")
def Dashboard(request, *args, **kwargs):
    payment = request.GET.get("payment_success", None)
    if payment and payment == "true":
        fancy_message(
            request,
            "Your Payment was successful and after review your campaign will start",
            level="success"
        )
    elif payment and payment == "false":
        fancy_message(request, "Payment failed", level="error")

    if is_admin(request.user):
        my_context = {
            "Title": f"Dashboard",
        }
        return render(request, "dashboard/admin/dashboard.html", my_context)
    else:
        queryset = Campaign.objects.filter(customer=request.user)[:7]
        queryset2 = Ticket.objects.filter(author=request.user)[:7]
        my_context = {
            "Title": f"Dashboard",
            "today": datetime.datetime.now(),
            "base_url": django_settings.EXTERNAL_API_BASE_URL,
            "campaigns": queryset,
            "tickets": queryset2,
        }
        return render(request, "dashboard/dashboard.html", my_context)


@login_required(login_url="/login")
def CampaignRetrieve(request, pk, *args, **kwargs):
    query = get_object_or_404(Campaign, id=pk, customer=request.user)

    my_context = {
        "Title": f"Campaign-{pk}",
        "campaign": query
    }
    return render(request, "dashboard/campaign_retrieve.html", my_context)


@login_required(login_url="/login")
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
                    form4 = CampaignAudioForm(
                        instance=campaign_audio,
                        data=request.POST,
                        files=request.FILES
                    )
                    if form4.is_valid():
                        campaign.email_template = CampaignEmailTemplate.objects.get(
                            id=selected_template
                        )
                        campaign.is_resubmit = True
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


@login_required(login_url="/login")
def CampaignActions(request, id, status, *args, **kwargs):
    queryset = get_object_or_404(Campaign, pk=id, customer_id=request.user.id)
    queryset.status = str(status)
    queryset.admin = request.user
    if status == "processing":
        queryset.is_resubmit = False
    queryset.save()
    fancy_message(request, f"Campaign-{id} : status changed to {status}", level="success")
    return redirect("campaign:dashboard")


@login_required(login_url="/login")
def CampaignList(request, *args, **kwargs):
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
    return render(request, "dashboard/campaign_list.html", my_context)


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def ListOfCampaignsType(request, *args, **kwargs):
    queryset = CampaignType.objects.filter(is_active=True)
    params = request.GET.get("id", None)
    if params:
        queryset = queryset.filter(id=params)
    serializer = [
        {
            "id": item.id,
            "name": item.name,
            "slug": item.slug,
            "price": item.price,
        }
        for item in queryset
    ]

    return JsonResponse(serializer, safe=False)


@csrf_exempt
def EmailPreview(request, pk, *args, **kwargs):
    if request.method == "POST":
        queryset = get_object_or_404(CampaignEmailTemplate, id=pk)
        content = request.POST.get("content", None)
        type = request.POST.get("type", None)

        if type:
            type_obj = get_object_or_404(CampaignEmailType, id=type)
            my_context = {
                "content": queryset.get_rendered_content(
                    {"body": content, "greeting": type_obj.name, "first_name": "john",
                     "last_name": "doe"}
                ),
                "type": type_obj.name
            }
        else:
            my_context = {
                "content": queryset.get_rendered_content({"body": content})
            }
        return HttpResponse(my_context.get("content"), status=200)
    else:
        return HttpResponse("get not allowed", status=400)


@transaction.atomic
@login_required(login_url="/login")
def CampaignCreate(request, *args, **kwargs):
    socials = SocialMedia.objects.filter(is_active=True).prefetch_related("social_media_fields")
    campaign_data = {}
    campaign_sms_data = {}
    campaign_email_data = {}

    if request.method == "POST":
        try:
            campaign_data["type"] = request.POST.getlist("type")[0]
            selected_template = request.POST.get("selected-template", None)

            # Consolidate campaign data
            campaign_sms_data.update(
                {
                    "type": request.POST.getlist("type")[1],
                    "body": request.POST.getlist("body")[0]
                }
            )

            campaign_email_data.update(
                {
                    "type": request.POST.getlist("type")[2],
                    "subject": request.POST.get("subject"),
                    "body": request.POST.getlist("body")[1]
                }
            )

            zip_selects = [
                int(request.POST.get(f"select-{i}", None))
                for i in range(1, 4)
                if request.POST.get(f"select-{i}", None) != "empty"
            ]

            if not zip_selects:
                fancy_message(request, "Please select zip codes", level="error")
                return redirect(request.path)

            form1 = CampaignForm(campaign_data)
            if not form1.is_valid():
                fancy_message(request, form1.errors, level="error")
                return redirect(request.path)

            if not selected_template:
                fancy_message(request, "Please select an email template", level="error")
                return redirect(request.path)

            form2 = CampaignSMSForm(campaign_sms_data)
            if not form2.is_valid():
                fancy_message(request, form2.errors, level="error")
                return redirect(request.path)

            form3 = CampaignEmailForm(campaign_email_data)
            if not form3.is_valid():
                fancy_message(request, form3.errors, level="error")
                return redirect(request.path)

            form4 = CampaignAudioForm(request.POST, files=request.FILES)
            if not form4.is_valid():
                fancy_message(request, form4.errors, level="error")
                return redirect(request.path)

            # Save the campaign object and its related data
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

            # Save social media entries
            for social in socials:
                social_media_data = {
                    field: request.POST.get(f"{social.object_name}_{field.object_name}")
                    for field in social.social_media_fields.all()
                    if request.POST.get(f"{social.object_name}_{field.object_name}")
                }
                social_media_upload_data = {
                    field: request.FILES.get(f"uploads_{social.object_name}_{field.object_name}")
                    for field in social.social_media_uploads.all()
                    if request.FILES.get(f"uploads_{social.object_name}_{field.object_name}")
                }

                print(social_media_upload_data)

                social_entry_form = CampaignSocialMediaEntryForm(
                    data={
                        "campaign": campaign_obj.id,
                        "social_media": social.id,
                        "post_frequency": request.POST.get(
                            f"{social.object_name}_post_frequency",
                            None
                        ),
                        "post_time": request.POST.get(f"{social.object_name}_post_time", None),
                    }
                )

                if (social_media_data or social_media_upload_data) and social_entry_form.is_valid():
                    entry = social_entry_form.save()

                    invalid = False

                    for field, value in social_media_data.items():
                        field_value_form = CampaignSocialMediaFieldValueForm(
                            data={
                                "entry": entry.id,
                                "field": field.id,
                                "value": value,
                            }
                        )
                        if field_value_form.is_valid():
                            field_value_form.save()
                        else:
                            invalid = True
                            fancy_message(request, field_value_form.errors, level="error")

                    for field, value in social_media_upload_data.items():
                        field_value_form = CampaignSocialMediaUploadFileForm(
                            data={
                                "entry": entry.id,
                                "upload": field.id,
                            },
                            files={"file": value}
                        )
                        if field_value_form.is_valid():
                            field_value_form.save()
                        else:
                            invalid = True
                            fancy_message(request, field_value_form.errors, level="error")

                    if invalid:
                        raise Exception("Invalid social media field value or file upload.")


            # Success message and redirect
            fancy_message(request, "New campaign successfully created", level="success")

            # Payment handling
            if request.POST.get("payment_method") == "pay":
                return redirect(f"/checkout/payment/{campaign_obj.id}/")

            return redirect("campaign:dashboard")
        except Exception as e:
            logger.exception(f"Unexpected error during campaign creation: {e}")
            fancy_message(
                request,
                "An error occurred during processing of campaign creation, please try later",
                level="error"
            )
            return redirect("campaign:campaignList")

    # Initialize the forms with existing data
    form1 = CampaignForm(initial=campaign_data)
    form2 = CampaignSMSForm(initial=campaign_sms_data)
    form3 = CampaignEmailForm(initial=campaign_email_data)
    form4 = CampaignAudioForm(initial=request.POST, files=request.FILES)
    frequency_choices = CampaignSocialMediaEntry.FrequencyChoices.choices

    # Additional context for the template
    zips = CampaignZip.objects.filter(is_active=True)
    email_templates = CampaignEmailTemplate.objects.filter(is_active=True)

    context = {
        "Title": "Campaign | Create",
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "zips": zips,
        "templates": email_templates,
        "socials": socials,
        "frequency_choices": frequency_choices,
    }

    return render(request, "dashboard/create_campaign.html", context)


def webhook(request, *args, **kwargs):
    if request.method == "POST":
        campaign_id = request.POST.get("campaign_id", None)
        status = request.POST.get("status", None)
        if not campaign_id:
            return HttpResponse("campaign_id is required", status=400)

        if not status:
            return HttpResponse("status is required", status=400)

        try:
            campaign = get_object_or_404(Campaign, id=campaign_id)
            campaign.status = status
            campaign.save()

            return HttpResponse("Done", status=200)

        except Exception as e:
            print(f"An error occurred: {e}")
            return HttpResponse(
                "something went wrong when trying change campaign status",
                status=500
            )
    else:
        return HttpResponse("method get is not allowed", status=400)
