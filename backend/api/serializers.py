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
        fields = '__all__'


class IndustryQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryQuestion
        fields = '__all__'


class UserIndustryAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIndustryAnswer
        fields = '__all__'
