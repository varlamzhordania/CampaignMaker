from django.urls import path
from .views import Dashboard, AdminCampaignList, AdminCampaignActions, CampaignCreate, CampaignRetrieve, EmailPreview, \
    AdminCampaignNote

app_name = 'campaign'

urlpatterns = [

    # user urls
    path("dashboard/", Dashboard, name="dashboard"),
    path("dashboard/preview/email/<int:pk>/", EmailPreview, name="emailPreview"),
    path("dashboard/campaign/create/", CampaignCreate, name="campaignCreate"),
    path("dashboard/campaign/<int:pk>/", CampaignRetrieve, name="campaignRetrieve"),
    path("dashboard/admin/campaigns/", AdminCampaignList, name="adminCampaigns"),
    path("dashboard/admin/campaigns/<int:id>/<str:status>/", AdminCampaignActions, name="adminCampaignsAction"),
    path("dashboard/admin/campaigns_note/", AdminCampaignNote, name="adminCampaignsNote"),
]
