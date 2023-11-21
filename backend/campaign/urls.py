from django.urls import path
from .views import Dashboard, CampaignCreate, CampaignResubmit, EmailPreview, ListOfEmailTemplates, CampaignActions, \
    ListOfCampaignsType, CampaignRetrieve, webhook, CampaignList

app_name = 'campaign'

urlpatterns = [
    path("dashboard/", Dashboard, name="dashboard"),
    path("dashboard/campaign/list/", CampaignList, name="campaignList"),
    path("dashboard/campaign/<int:pk>/", CampaignRetrieve, name="campaignRetrieve"),
    path("dashboard/preview/email/<int:pk>/", EmailPreview, name="emailPreview"),
    path("dashboard/campaign/create/", CampaignCreate, name="campaignCreate"),
    path("dashboard/campaign/resubmit/<int:pk>/", CampaignResubmit, name="campaignResubmit"),
    path("dashboard/campaigns/<int:id>/<str:status>/", CampaignActions, name="campaignsAction"),
    path("dashboard/email/templates/", ListOfEmailTemplates, name="emailTemplatesList"),
    path("dashboard/campaign/types/", ListOfCampaignsType, name="campaignTypeList"),
    path("dashboard/campaign/webhook/", webhook, name="webhook"),
]
