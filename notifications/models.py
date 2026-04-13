from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPES = [
        ("like",    "Curtiu seu tweet"),
        ("comment", "Comentou no seu tweet"),
        ("retweet", "Retweetou seu tweet"),
        ("follow",  "Começou a te seguir"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )
    notif_type = models.CharField(max_length=10, choices=TYPES)
    tweet = models.ForeignKey(
        "tweets.Tweet",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} → {self.recipient} ({self.notif_type})"
