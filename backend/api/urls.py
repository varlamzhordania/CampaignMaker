from django.urls import path
from .views import IndustryListAPIView, IndustryQuestionListAPIView, \
    UserBusinessProfileAndQuestionsApiView

app_name = 'api'

urlpatterns = [
    path("industry/", IndustryListAPIView.as_view(), name="industry"),
    path("industry/questions/", IndustryQuestionListAPIView.as_view(), name="industry_questions"),
    path(
        "user/business/profile/",
        UserBusinessProfileAndQuestionsApiView.as_view(),
        name="user_business_profile"
    ),
]
