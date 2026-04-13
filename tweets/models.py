from django.db import models
from django.conf import settings


class Tweet(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tweets",
    )
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to="tweet_media/images/", blank=True, null=True)
    video = models.FileField(upload_to="tweet_media/videos/", blank=True, null=True)

    # retweet aponta para outro tweet (opcional)
    retweet_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="retweets",
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_tweets",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def likes_count(self):
        return self.likes.count()

    def retweets_count(self):
        return self.retweets.count()

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f"@{self.author.username}: {self.content[:50]}"


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"@{self.author.username} → tweet {self.tweet_id}"
