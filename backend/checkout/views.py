from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from campaign.models import Campaign
from .models import CampaignTransaction
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY
domain = settings.STRIPE_BASE_DOMAIN


def fulfill_order(id):
    transaction = CampaignTransaction.objects.get(payment_id=id)
    if transaction:
        transaction.status = "COMPLETED"
        transaction.save()
        campaign = Campaign.objects.get(campaign_transaction__id=transaction.id)
        campaign.status = "wait"
        campaign.save()
        print("Fulfilling order")
    else:
        print(f"failed to find transaction with id : {id}")


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id']
        )
        fulfill_order(session.id)
        return HttpResponse(status=200)
    if event['type'] == 'payment_intent.succeeded':
        return HttpResponse(status=200)

    print(event["type"])
    return HttpResponse(500)


def Checkout(request, pk, *args, **kwargs):
    queryset = Campaign.objects.filter(pk=pk).first()
    if queryset:
        try:
            checkout = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": queryset.type.name,
                            },
                            "unit_amount": int(queryset.type.price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=domain + "/dashboard?payment_success=true",
                cancel_url=domain + "/dashboard?payment_success=false"
            )
            campaign_transaction = CampaignTransaction.objects.filter(campaign_id=queryset.id)
            if campaign_transaction.exists():
                campaign_transaction.update(
                    campaign_id=queryset.id,
                    customer_id=request.user.id,
                    amount=queryset.type.price,
                    payment_id=checkout.id,
                    currency="usd",
                    gateway="stripe",
                    status="PENDING"
                )
            else:
                CampaignTransaction.objects.create(
                    campaign_id=queryset.id,
                    customer_id=request.user.id,
                    amount=queryset.type.price,
                    payment_id=checkout.id,
                    currency="usd",
                    gateway="stripe",
                    status="PENDING"

                )
            return redirect(checkout.url)
        except Exception as e:
            return HttpResponse(e)

    else:
        return HttpResponse("invalid url", status=400)
