from .models import Notification


def create_notification(recipient, sender, notif_type, tweet=None):
    """Cria uma notificação. Não cria duplicatas para follow."""
    if recipient == sender:
        return
    if notif_type == "follow":
        Notification.objects.get_or_create(
            recipient=recipient, sender=sender, notif_type="follow"
        )
    else:
        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notif_type=notif_type,
            tweet=tweet,
        )
