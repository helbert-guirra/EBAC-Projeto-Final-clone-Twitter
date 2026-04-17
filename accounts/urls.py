from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path("password/", views.change_password, name="change_password"),
    path("follow/<int:user_id>/", views.follow_toggle, name="follow_toggle"),
    path("search/", views.search_users, name="search"),  # ← antes do <str:username>
    path("<str:username>/", views.profile_view, name="profile"),
    path("<str:username>/followers/", views.followers_list, name="followers"),
    path("<str:username>/following/", views.following_list, name="following"),
]