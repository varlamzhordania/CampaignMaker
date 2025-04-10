# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from core.rabbitmq import RabbitMQPublisher

from .models import Campaign
from .serializers import RabbitMQCampaignSerializer


@receiver(pre_save, sender=Campaign)
def cache_previous_status(sender, instance, **kwargs):
    """Save previous status for comparison in post_save."""
    if instance.pk:
        try:
            old_instance = Campaign.objects.get(pk=instance.pk)
            instance._previous_status = old_instance.status
        except Campaign.DoesNotExist:
            instance._previous_status = None


@receiver(post_save, sender=Campaign)
def publish_to_rabbitmq_on_processing(sender, instance, created, **kwargs):
    """Publish to RabbitMQ when status changes to 'processing'."""
    previous_status = getattr(instance, "_previous_status", None)
    if previous_status != "processing" and instance.status == "processing":
        serializer = RabbitMQCampaignSerializer(instance)
        print("Serializing data for rabbitmq", serializer.data)
        publisher = RabbitMQPublisher()
        print("Publishing to RabbitMQ")
        publisher.publish_message(serializer.data)
        print("Published to RabbitMQ")
        publisher.close_connection()
        print("Closed connection to RabbitMQ")
