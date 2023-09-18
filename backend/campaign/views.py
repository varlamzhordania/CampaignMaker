from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/")
def Dashboard(request, *args, **kwargs):
    my_context = {"Title": f"Dashboard | {request.user.username}", }
    return render(request, "dashboard/dashboard.html", my_context)


