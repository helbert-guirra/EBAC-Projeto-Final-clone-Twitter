from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("tweet/new/", views.create_tweet, name="create_tweet"),
    path("tweet/<int:tweet_id>/delete/", views.delete_tweet, name="delete_tweet"),
    path("tweet/<int:tweet_id>/like/", views.like_toggle, name="like_toggle"),
    path("tweet/<int:tweet_id>/retweet/", views.retweet_toggle, name="retweet_toggle"),
    path("tweet/<int:tweet_id>/comment/", views.add_comment, name="add_comment"),
]
