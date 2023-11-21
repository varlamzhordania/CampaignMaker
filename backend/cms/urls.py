from django.urls import path
from .views import AdminCampaignActions, AdminCampaignAudio, AdminCampaignNote, AdminCampaignList, ListOfCampaigns, \
    AdminTicketList, AdminContactList, AdminTicketRetrieve

app_name = 'cms'

urlpatterns = [
    path("dashboard/admin/campaigns/<int:id>/<str:status>/", AdminCampaignActions, name="adminCampaignsAction"),
    path("dashboard/admin/campaigns_note/", AdminCampaignNote, name="adminCampaignsNote"),
    path("dashboard/admin/campaigns_audio/", AdminCampaignAudio, name="adminCampaignsAudio"),
    path("dashboard/admin/campaigns/list/", ListOfCampaigns, name="adminCampaignsList"),
    path("dashboard/admin/campaigns/", AdminCampaignList, name="adminCampaigns"),
    path("dashboard/admin/tickets/", AdminTicketList, name="adminTickets"),
    path("dashboard/admin/tickets/<int:pk>/", AdminTicketRetrieve, name="adminTicketRetrieve"),
    path("dashboard/admin/contacts/", AdminContactList, name="adminContacts"),
]
