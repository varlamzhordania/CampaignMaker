from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from account.models import Industry, IndustryQuestion, UserBusinessProfile, BusinessAudience, \
    UserIndustryAnswer
from campaign.models import CampaignEmailTemplate, CampaignAudio

from .serializers import IndustrySerializer, IndustryQuestionSerializer, \
    UserBusinessProfileSerializer, BusinessAudienceSerializer, CampaignEmailTemplateSerializer, \
    CampaignAudioSerializer


class IndustryListAPIView(ListAPIView):
    queryset = Industry.objects.filter(is_active=True)
    serializer_class = IndustrySerializer
    pagination_class = None


class IndustryQuestionListAPIView(ListAPIView):
    queryset = IndustryQuestion.objects.filter(is_active=True)
    serializer_class = IndustryQuestionSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['industry']


class UserBusinessProfileAndQuestionsApiView(APIView):
    serializer_classes = [UserBusinessProfileSerializer, BusinessAudienceSerializer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        data = request.data.copy()

        try:
            with transaction.atomic():

                business_data = data.get('business', {})
                business_profile, created = UserBusinessProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        "business_name": business_data.get("business_name"),
                        "industry_id": business_data.get("industry"),
                        "location": business_data.get("location"),
                        "website": business_data.get("website", ""),
                        "work_hours": business_data.get("work_hours"),
                        "brand_tone": business_data.get("brand_tone"),
                        "brand_keywords": business_data.get("brand_keywords", ""),
                    }
                )

                audience_data = data.get('audience', {})
                audience_profile, created = BusinessAudience.objects.update_or_create(
                    business=business_profile,
                    defaults={
                        "gender": audience_data.get("gender"),
                        "age_range": audience_data.get("age_range"),
                        "interests": audience_data.get("interests", ""),
                        "focus": audience_data.get("focus", ""),
                    }
                )

                questions_data = data.get('questions', {})

                for question_key, answer in questions_data.items():
                    question_id = question_key.split('_')[1]
                    try:
                        question = IndustryQuestion.objects.get(id=question_id)

                        UserIndustryAnswer.objects.update_or_create(
                            user=user,
                            question=question,
                            defaults={
                                "answer": dict({question.name: answer}),
                                "answered": True
                            }
                        )
                    except IndustryQuestion.DoesNotExist:
                        continue

                user.completed_questions()

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error processing data: {e}")
            return Response(
                {"detail": "There was an error processing your data."},
                status=status.HTTP_400_BAD_REQUEST
            )


class EmailTemplateRetrieveSlugView(RetrieveAPIView):
    queryset = CampaignEmailTemplate.objects.filter(is_active=True)
    serializer_class = CampaignEmailTemplateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'


class CampaignAudioRetrieveView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = CampaignAudio.objects.all()
    serializer_class = CampaignAudioSerializer
