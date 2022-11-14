from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.
def index(request):
    return render(request, "chat/index.html")


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
            "user": "anonymouse",
            "userid": "anonymouse",
        }
    return render(request, "chat/room.html", context)
