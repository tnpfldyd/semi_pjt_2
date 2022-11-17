from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json

# Create your views here.


@login_required
def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    if request.user.is_authenticated:
        context = {
            "room_name": room_name,
            "user": request.user.nickname,
            "userid": request.user.username,
        }
    else:
        context = {
            "room_name": room_name,
            "user": "Anonymouse",
            "userid": "Anonymouse",
        }
    return render(request, "chat/room.html", context)
