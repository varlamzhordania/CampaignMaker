from django.urls import path
from .views import Dashboard, AdminCampaignList, AdminCampaignActions,CampaignCreate,CampaignRetrieve

app_name = 'campaign'

urlpatterns = [

    # user urls
    path("dashboard/", Dashboard, name="dashboard"),
    path("dashboard/campaign/create/", CampaignCreate, name="campaignCreate"),
    path("dashboard/campaign/<int:pk>/", CampaignRetrieve, name="campaignRetrieve"),
    path("dashboard/admin/campaigns/", AdminCampaignList, name="adminCampaigns"),
    path("dashboard/admin/campaigns/<int:id>/<str:status>/", AdminCampaignActions, name="adminCampaignsAction"),
]
