from django.urls import path
from .views import Dashboard

app_name = 'campaign'

urlpatterns = [

    # user urls
    path("dashboard/", Dashboard, name="dashboard"),
]
