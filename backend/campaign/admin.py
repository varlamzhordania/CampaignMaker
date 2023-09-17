from django.contrib import admin
from .models import CampaignZip, CampaignAudio, CampaignSMS, CampaignType, CampaignSMSType, Campaign, CampaignEmail, \
    CampaignEmailType
# Register your models here.

admin.site.register(CampaignZip)
admin.site.register(CampaignAudio)
admin.site.register(CampaignSMS)
admin.site.register(CampaignType)
admin.site.register(CampaignSMSType)
admin.site.register(Campaign)
admin.site.register(CampaignEmail)
admin.site.register(CampaignEmailType)