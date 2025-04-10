from rest_framework import serializers
from django.conf import settings

from .models import Campaign, CampaignZip, CampaignSMS, CampaignEmail, CampaignAudio, CampaignEmailTemplate


class CampaignEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignEmailTemplate
        fields = ['id', 'name', 'slug', 'template', 'extra']


class CampaignZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignZip
        fields = ['id', 'name', 'slug', 'code']


class CampaignSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSMS
        fields = ['id', 'type', 'body']


class CampaignEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignEmail
        fields = ['id', 'type', 'subject', 'body']


class CampaignAudioSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = CampaignAudio
        fields = ['id', 'text', 'file']

    def get_file(self, obj):
        return f"{settings.BASE_DOMAIN}{obj.file.url}" if obj.file else None


class RabbitMQCampaignSerializer(serializers.ModelSerializer):
    zips = CampaignZipSerializer(many=True, read_only=True)
    campaign_sms = CampaignSMSSerializer(read_only=True)
    campaign_email = CampaignEmailSerializer(read_only=True)
    campaign_audio = CampaignAudioSerializer(read_only=True)
    email_template = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'status', 'date_start', 'create_at', 'update_at', 'customer', 'admin', 'type', 'email_template',
                  'zips', 'campaign_sms', 'campaign_email', 'campaign_audio']

    def get_email_template(self, obj):
        data = CampaignEmailTemplateSerializer(obj.email_template).data
        data['template'] = settings.BASE_DOMAIN + data['template']
        return data
