from rest_framework import serializers

from .models import (
    Campaign, CampaignZip, CampaignSMS, CampaignEmail, CampaignAudio,
    CampaignEmailTemplate, CampaignSocialMediaEntry, CampaignSocialMediaFieldValue,
)


class CampaignEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignEmailTemplate
        fields = ['id', 'name', 'slug']


class CampaignZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignZip
        fields = ['id', 'name', 'slug', 'code', 'timezone_name', 'timezone_offset']


class CampaignSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSMS
        fields = ['id', 'type', 'body']


class CampaignEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignEmail
        fields = ['id', 'type', 'subject', 'body']


class CampaignAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignAudio
        fields = ['id']


class SocialMediaFieldValueSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = CampaignSocialMediaFieldValue
        fields = ['key', 'value']

    def get_key(self, obj):
        if obj.field:
            return obj.field.object_name
        return None


class SocialMediaEntrySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    entry_fields = serializers.SerializerMethodField()

    class Meta:
        model = CampaignSocialMediaEntry
        fields = ["name", "post_frequency", "post_time", "entry_fields", ]

    def get_entry_fields(self, obj):
        queryset = CampaignSocialMediaFieldValue.objects.filter(entry_id=obj.pk)

        return SocialMediaFieldValueSerializer(queryset, many=True).data

    def get_name(self, obj):
        return obj.social_media.object_name


class RabbitMQCampaignSerializer(serializers.ModelSerializer):
    zips = CampaignZipSerializer(many=True, read_only=True)
    campaign_sms = CampaignSMSSerializer(read_only=True)
    campaign_email = CampaignEmailSerializer(read_only=True)
    campaign_audio = CampaignAudioSerializer(read_only=True)
    email_template = CampaignEmailTemplateSerializer(read_only=True)
    socials = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'status', 'date_start', 'created_at', 'updated_at', 'customer', 'admin',
                  'type', 'email_template',
                  'zips', 'campaign_sms', 'campaign_email', 'campaign_audio', 'socials']

    def get_socials(self, obj):
        entries = obj.campaign_social_media_entry.all()
        list_socials = []
        for entry in entries:
            serializer = SocialMediaEntrySerializer(entry)
            list_socials.append(serializer.data)

        return list_socials
