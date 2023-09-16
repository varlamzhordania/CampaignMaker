from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(user_logged_in, sender=get_user_model())
def update_last_ip_address(sender, request, user, **kwargs):
    user.last_ip = request.META.get('REMOTE_ADDR')
    user.save()

