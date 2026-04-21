from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.shortcuts import render

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("tweets.urls")),
    path("notifications/", include("notifications.urls")),
    path("teste-404/", lambda request: render(request, '404.html', status=404)),
    path("", RedirectView.as_view(url="/feed/", permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def handler404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = handler404_view
