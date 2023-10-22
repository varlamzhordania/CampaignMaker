from django.urls import path
from .views import home, category

app_name = 'main'

urlpatterns = [
    path("", home, name="home"),
    path("category/<slug:slug>/", category, name="category")
]
