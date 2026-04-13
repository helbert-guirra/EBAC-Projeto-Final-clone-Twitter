from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import JsonResponse

from .models import User
from .forms import RegisterForm, ProfileForm, CustomPasswordChangeForm
from notifications.utils import create_notification


def register(request):
    if request.user.is_authenticated:
        return redirect("feed")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("feed")
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    pass


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    tweets = user.tweets.select_related("author").prefetch_related("likes").order_by("-created_at")
    is_following = request.user.following.filter(pk=user.pk).exists()
    return render(request, "accounts/profile.html", {
        "profile_user": user,
        "tweets": tweets,
        "is_following": is_following,
    })


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("profile", username=request.user.username)
    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)   # mantém o usuário logado
        messages.success(request, "Senha alterada com sucesso!")
        return redirect("profile", username=request.user.username)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def follow_toggle(request, user_id):
    """Seguir/deixar de seguir via AJAX (POST)."""
    if request.method != "POST":
        return JsonResponse({"error": "método não permitido"}, status=405)

    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return JsonResponse({"error": "você não pode seguir a si mesmo"}, status=400)

    if request.user.following.filter(pk=target.pk).exists():
        request.user.following.remove(target)
        following = False
    else:
        request.user.following.add(target)
        following = True
        create_notification(
            recipient=target,
            sender=request.user,
            notif_type="follow",
        )

    return JsonResponse({
        "following": following,
        "followers_count": target.followers_count(),
    })


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/follow_list.html", {
        "profile_user": user,
        "users": user.followers.all(),
        "title": "Seguidores",
    })


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/follow_list.html", {
        "profile_user": user,
        "users": user.following.all(),
        "title": "Seguindo",
    })
