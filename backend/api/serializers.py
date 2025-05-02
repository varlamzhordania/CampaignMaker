from rest_framework import serializers
from account.models import Industry, IndustryQuestion, UserIndustryAnswer, User, \
    UserBusinessProfile, \
    BusinessAudience
from campaign.models import CampaignEmailTemplate, CampaignAudio


class CampaignAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignAudio
        fields = '__all__'


class CampaignEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignEmailTemplate
        fields = '__all__'


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name', 'is_active']


class UserBusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBusinessProfile
        fields = '__all__'


class BusinessAudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAudience
        exclude = ["created_at", "updated_at"]


class IndustryQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryQuestion
        fields = '__all__'


class UserIndustryAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIndustryAnswer
        fields = ["id", "answer", "answered", ]


class UserBusinessFullProfileSerializer(serializers.ModelSerializer):
    business_audience = BusinessAudienceSerializer(read_only=True)
    industry_answers = UserIndustryAnswerSerializer(
        many=True,
        read_only=True,
        source='user.industry_answers'
    )
    industry = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserBusinessProfile
        fields = [
            'id', 'user', 'business_name', 'industry', 'location', 'website', 'work_hours',
            'brand_tone', 'brand_keywords', 'business_audience', 'industry_answers'
        ]
