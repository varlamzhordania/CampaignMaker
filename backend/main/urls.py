from django.urls import path
from .views import home, category, contact_us, about_us, privacy_policy, terms, refund, feedback

app_name = 'main'

urlpatterns = [
    path("", home, name="home"),
    path("about/", about_us, name="about"),
    path("contact/", contact_us, name="contact"),
    path("privacy/", privacy_policy, name="privacy"),
    path("terms/", terms, name="terms"),
    path("refund/", refund, name="refund"),
    path("feedback/", feedback, name="feedback"),
    path("category/<slug:slug>/", category, name="category")
]
