from django.contrib import admin
from .models import CampaignTransaction


# Register your models here.

class AdminCampaignTransaction(admin.ModelAdmin):
    list_display = ["id", "campaign", "customer", "payment_id", "amount", "currency", "gateway", "status", "created_at",
                    "updated_at"]
    list_filter = ["currency", "gateway", "status", "created_at", "updated_at"]


admin.site.register(CampaignTransaction, AdminCampaignTransaction)
