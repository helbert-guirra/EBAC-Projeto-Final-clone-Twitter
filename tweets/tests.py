from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from tweets.models import Tweet, Comment


class FeedTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="helbert", password="senhaforte123!")
        self.client.login(username="helbert", password="senhaforte123!")

    def test_feed_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("feed"))
        self.assertRedirects(response, "/accounts/login/?next=/feed/")

    def test_feed_loads_for_authenticated_user(self):
        response = self.client.get(reverse("feed"))
        self.assertEqual(response.status_code, 200)

    def test_feed_shows_own_tweets(self):
        Tweet.objects.create(author=self.user, content="meu tweet")
        response = self.client.get(reverse("feed"))
        self.assertContains(response, "meu tweet")

    def test_feed_shows_followed_users_tweets(self):
        other = User.objects.create_user(username="outro", password="senhaforte123!")
        self.user.following.add(other)
        Tweet.objects.create(author=other, content="tweet do seguido")
        response = self.client.get(reverse("feed"))
        self.assertContains(response, "tweet do seguido")

    def test_feed_does_not_show_unfollowed_tweets(self):
        other = User.objects.create_user(username="outro", password="senhaforte123!")
        Tweet.objects.create(author=other, content="tweet invisivel")
        response = self.client.get(reverse("feed"))
        self.assertNotContains(response, "tweet invisivel")


class TweetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="helbert", password="senhaforte123!")
        self.client.login(username="helbert", password="senhaforte123!")

    def test_create_tweet(self):
        self.client.post(reverse("create_tweet"), {"content": "olá mundo"})
        self.assertTrue(Tweet.objects.filter(content="olá mundo").exists())

    def test_delete_tweet(self):
        tweet = Tweet.objects.create(author=self.user, content="apaga isso")
        self.client.post(reverse("delete_tweet", kwargs={"tweet_id": tweet.pk}))
        self.assertFalse(Tweet.objects.filter(pk=tweet.pk).exists())

    def test_cannot_delete_other_users_tweet(self):
        other = User.objects.create_user(username="outro", password="senhaforte123!")
        tweet = Tweet.objects.create(author=other, content="tweet do outro")
        response = self.client.post(reverse("delete_tweet", kwargs={"tweet_id": tweet.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(pk=tweet.pk).exists())


class LikeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="helbert", password="senhaforte123!")
        self.other = User.objects.create_user(username="outro", password="senhaforte123!")
        self.tweet = Tweet.objects.create(author=self.other, content="tweet para curtir")
        self.client.login(username="helbert", password="senhaforte123!")

    def test_like_tweet(self):
        response = self.client.post(reverse("like_toggle", kwargs={"tweet_id": self.tweet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.tweet.likes.filter(pk=self.user.pk).exists())

    def test_unlike_tweet(self):
        self.tweet.likes.add(self.user)
        self.client.post(reverse("like_toggle", kwargs={"tweet_id": self.tweet.pk}))
        self.assertFalse(self.tweet.likes.filter(pk=self.user.pk).exists())


class CommentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="helbert", password="senhaforte123!")
        self.tweet = Tweet.objects.create(author=self.user, content="tweet comentado")
        self.client.login(username="helbert", password="senhaforte123!")

    def test_add_comment(self):
        response = self.client.post(
            reverse("add_comment", kwargs={"tweet_id": self.tweet.pk}),
            {"content": "bom tweet!"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content="bom tweet!").exists())
