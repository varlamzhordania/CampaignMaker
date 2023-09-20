from django.db import models
from campaign.models import Campaign
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

STATUS_PAYMENT_CHOICES = (
    ("PENDING", "Pending"),
    ("UNCOMPLETED", "UnCompleted"),
    ("COMPLETED", "Completed"),
)


class CampaignTransaction(models.Model):
    campaign = models.OneToOneField(
        Campaign, related_name="campaign_transaction", on_delete=models.CASCADE,
        verbose_name=_("Campaign"),
        blank=False, null=False
    )
    customer = models.ForeignKey(
        get_user_model(), blank=True, unique=False, null=True, related_name="user_campaign_transaction",
        verbose_name=_("Customer"),
        on_delete=models.CASCADE
    )
    payment_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    client_secret = models.CharField(max_length=255, null=True, blank=True, unique=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("amount have to pay"),
        help_text=_("format : maximum amount 99999.99"),
        error_messages={
            "name": {
                "max_length": _("the amount must be between 0 and 99999.99"),
            },
        },
    )
    status = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("payment status"),
        choices=STATUS_PAYMENT_CHOICES, default="PENDING",
        help_text=_(
            "format : Pending = waiting for payment , UnCompleted = payed a specific amount or half , Completed = payment fullfilled and complete"
        )
    )

    gateway = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("payment method"),
        help_text=_("format : credit,debit,mastercard,paypal...etc")
    )

    create_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date payment created"),
        help_text=_("format : y-m-d H:M:S")
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date payment last updated"),
        help_text=_("format : y-m-d H:M:S")
    )

    def __str__(self):
        return f"{self.customer} : {self.payment_id}"
