# notifications/utils.py (NEW FILE in VS Code)
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target):
    """Creates a Notification instance."""
    # Prevent users from notifying themselves for their own actions
    if recipient.id == actor.id:
        return

    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=ContentType.objects.get_for_model(target),
        object_id=target.pk,
        target=target,
    )