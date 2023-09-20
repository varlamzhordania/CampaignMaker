from django.contrib import admin
from .models import CampaignTransaction


# Register your models here.

class AdminCampaignTransaction(admin.ModelAdmin):
    list_display = ["id", "campaign", "customer", "payment_id", "amount", "currency", "gateway", "status", "create_at",
                    "update_at"]
    list_filter = ["currency", "gateway", "status", "create_at", "update_at"]


admin.site.register(CampaignTransaction, AdminCampaignTransaction)
