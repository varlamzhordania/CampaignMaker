from django.urls import path
from .views import Dashboard, AdminCampaignList, AdminCampaignActions, CampaignCreate, CampaignResubmit, EmailPreview, \
    AdminCampaignNote, AdminCampaignAudio, ListOfEmailTemplates, CampaignActions, ListOfCampaignsType, ListOfCampaigns

app_name = 'campaign'

urlpatterns = [

    # user urls
    path("dashboard/", Dashboard, name="dashboard"),
    path("dashboard/preview/email/<int:pk>/", EmailPreview, name="emailPreview"),
    path("dashboard/campaign/create/", CampaignCreate, name="campaignCreate"),
    path("dashboard/campaign/resubmit/<int:pk>/", CampaignResubmit, name="campaignResubmit"),
    path("dashboard/admin/campaigns/", AdminCampaignList, name="adminCampaigns"),
    path("dashboard/campaigns/<int:id>/<str:status>/", CampaignActions, name="campaignsAction"),
    path("dashboard/admin/campaigns/<int:id>/<str:status>/", AdminCampaignActions, name="adminCampaignsAction"),
    path("dashboard/admin/campaigns_note/", AdminCampaignNote, name="adminCampaignsNote"),
    path("dashboard/admin/campaigns_audio/", AdminCampaignAudio, name="adminCampaignsAudio"),
    path("dashboard/admin/campaigns/list/", ListOfCampaigns, name="adminCampaignsList"),
    path("dashboard/email/templates/", ListOfEmailTemplates, name="emailTemplatesList"),
    path("dashboard/campaign/types/", ListOfCampaignsType, name="campaignTypeList"),
]
