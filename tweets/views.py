from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from accounts.models import User
from .models import Tweet, Comment
from .forms import TweetForm, CommentForm
from notifications.utils import create_notification


@login_required
def feed(request):
    following_ids = request.user.following.values_list("id", flat=True)
    tweets = (
        Tweet.objects
        .filter(author_id__in=[*following_ids, request.user.id])
        .select_related("author", "retweet_of__author")
        .prefetch_related("likes", "comments")
        .order_by("-created_at")
    )
    # Usuários que  ainda não segue (exceto eu mesmo)
    suggested_users = (
        User.objects.exclude(id=request.user.id)
        .exclude(id__in=following_ids)
        .order_by("?")[:5]
    )
    form = TweetForm()
    return render(request, "tweets/feed.html", {
        "tweets": tweets,
        "form": form,
        "suggested_users": suggested_users,
    })

@login_required
@require_POST
def create_tweet(request):
    form = TweetForm(request.POST, request.FILES)
    if form.is_valid():
        tweet = form.save(commit=False)
        tweet.author = request.user
        tweet.save()
    return redirect("feed")


@login_required
@require_POST
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, author=request.user)
    tweet.delete()
    return redirect("feed")


@login_required
@require_POST
def like_toggle(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.likes.filter(pk=request.user.pk).exists():
        tweet.likes.remove(request.user)
        liked = False
    else:
        tweet.likes.add(request.user)
        liked = True
        if tweet.author != request.user:
            create_notification(
                recipient=tweet.author,
                sender=request.user,
                notif_type="like",
                tweet=tweet,
            )
    return JsonResponse({"liked": liked, "count": tweet.likes_count()})


@login_required
@require_POST
def retweet_toggle(request, tweet_id):
    original = get_object_or_404(Tweet, pk=tweet_id)
    existing = Tweet.objects.filter(author=request.user, retweet_of=original).first()
    if existing:
        existing.delete()
        retweeted = False
    else:
        Tweet.objects.create(
            author=request.user,
            content=original.content,
            retweet_of=original,
        )
        retweeted = True
        if original.author != request.user:
            create_notification(
                recipient=original.author,
                sender=request.user,
                notif_type="retweet",
                tweet=original,
            )
    return JsonResponse({"retweeted": retweeted, "count": original.retweets_count()})


@login_required
@require_POST
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.tweet = tweet
        comment.author = request.user
        comment.save()
        if tweet.author != request.user:
            create_notification(
                recipient=tweet.author,
                sender=request.user,
                notif_type="comment",
                tweet=tweet,
            )
        return JsonResponse({
            "success": True,
            "username": request.user.username,
            "avatar": request.user.get_avatar_url(),
            "content": comment.content,
            "count": tweet.comments_count(),
        })
    return JsonResponse({"success": False}, status=400)
