from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notification_list(request):
    notifications = request.user.notifications.select_related("sender", "tweet").all()
    # marca todas como lidas ao abrir a página
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, "notifications/list.html", {"notifications": notifications})
