from django.urls import path
from .views import (
    IndustryListAPIView, IndustryQuestionListAPIView,
    UserBusinessProfileAndQuestionsApiView, EmailTemplateRetrieveSlugView,
    CampaignAudioRetrieveView, UserBusinessFullProfileAPIView,CampaignSocialUploadRetrieveView
)

app_name = 'api'

urlpatterns = [
    path("industry/", IndustryListAPIView.as_view(), name="industry"),
    path("industry/questions/", IndustryQuestionListAPIView.as_view(), name="industry_questions"),
    path(
        "user/business/profile/",
        UserBusinessProfileAndQuestionsApiView.as_view(),
        name="user_business_profile"
    ),
    path(
        "user/business/profile/<int:user_id>/",
        UserBusinessFullProfileAPIView.as_view(),
        name="user_business_full_profile"
    ),

    path(
        "campaign/email/template/<slug:slug>/",
        EmailTemplateRetrieveSlugView.as_view(),
        name="campaign_email_template"
    ),
    path(
        "campaign/audio/<int:pk>/",
        CampaignAudioRetrieveView.as_view(),
        name="campaign_email"
    ),
    path(
        "campaign/social/upload/<int:pk>/",
        CampaignSocialUploadRetrieveView.as_view(),
        name="campaign_social_upload"
    ),
]
