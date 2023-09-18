from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CampaignForm
from .models import CampaignZip


# Create your views here.

@login_required(login_url="/")
def Dashboard(request, *args, **kwargs):
    form1 = CampaignForm()
    zips = CampaignZip.objects.filter(is_active=True)
    if request.method == "POST":
        print(request.POST)
    my_context = {"Title": f"Dashboard | {request.user.username}", "form1": form1, "zips": zips}
    return render(request, "dashboard/dashboard.html", my_context)
