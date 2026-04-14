from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from tweets.models import Tweet
from notifications.models import Notification
from notifications.utils import create_notification


class NotificationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="helbert", password="senhaforte123!")
        self.other = User.objects.create_user(username="outro", password="senhaforte123!")
        self.tweet = Tweet.objects.create(author=self.user, content="tweet teste")
        self.client.login(username="helbert", password="senhaforte123!")

    def test_notification_page_loads(self):
        response = self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)

    def test_like_creates_notification(self):
        self.client.login(username="outro", password="senhaforte123!")
        self.client.post(reverse("like_toggle", kwargs={"tweet_id": self.tweet.pk}))
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user,
                sender=self.other,
                notif_type="like"
            ).exists()
        )

    def test_follow_creates_notification(self):
        self.client.login(username="outro", password="senhaforte123!")
        self.client.post(reverse("follow_toggle", kwargs={"user_id": self.user.pk}))
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user,
                sender=self.other,
                notif_type="follow"
            ).exists()
        )

    def test_notifications_marked_as_read_on_visit(self):
        Notification.objects.create(
            recipient=self.user,
            sender=self.other,
            notif_type="follow",
            is_read=False,
        )
        self.client.get(reverse("notifications"))
        self.assertFalse(
            Notification.objects.filter(recipient=self.user, is_read=False).exists()
        )

    def test_no_self_notification(self):
        create_notification(recipient=self.user, sender=self.user, notif_type="like", tweet=self.tweet)
        self.assertFalse(
            Notification.objects.filter(recipient=self.user, sender=self.user).exists()
        )
