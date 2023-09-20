from django.urls import path
from .views import Dashboard, AdminCampaignList,AdminCampaignActions

app_name = 'campaign'

urlpatterns = [

    # user urls
    path("dashboard/", Dashboard, name="dashboard"),
    path("dashboard/campaigns/", AdminCampaignList, name="adminCampaigns"),
    path("dashboard/campaigns/<int:id>/<str:status>/", AdminCampaignActions, name="adminCampaignsAction"),
]
