from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuário customizado. Herda tudo do AbstractUser (username, email, password…)
    e adiciona os campos extras do Twitter.
    """
    bio = models.TextField(blank=True, max_length=160)
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True,
        default=None
    )
    cover = models.ImageField(
        upload_to="covers/", blank=True, null=True,
        default=None
    )
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        name = self.get_full_name() or self.username
        return f"https://api.dicebear.com/7.x/initials/svg?seed={name}&backgroundColor=1d9bf0&fontFamily=Arial&fontSize=40&fontWeight=700"

    def get_cover_url(self):
        if self.cover:
            return self.cover.url
        return None

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def __str__(self):
        return f"@{self.username}"