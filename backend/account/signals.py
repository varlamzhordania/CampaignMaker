import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


@receiver(user_logged_in, sender=get_user_model())
def update_last_ip_address(sender, request, user, **kwargs):
    ip_address = request.META.get('REMOTE_ADDR')

    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        ip_address = forwarded_for.split(',')[0]

    if not ip_address:
        logger.warning(f"Failed to retrieve IP address for user {user.id}")
        return

    if user.last_ip != ip_address:
        user.last_ip = ip_address
        user.save(update_fields=['last_ip'])
        logger.info(f"Updated last IP address for user {user.id} to {ip_address}")
    else:
        logger.info(f"User {user.id} logged in from the same IP: {ip_address}")
