from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.http import JsonResponse


@login_required
def index(request):
    notes = request.user.user_to.order_by("-created_at")
    to_notes = request.user.user_from.order_by("-created_at")

    return render(request, "notes/index.html", {"notes": notes, "to_notes": to_notes},)


@login_required
def send(request, pk):
    to_user = get_object_or_404(get_user_model(), pk=pk)
    form = NotesForm(request.POST or None)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.from_user = request.user
        temp.to_user = to_user
        temp.save()
        messages.success(request, "쪽지 전송 완료.😀")
        return redirect("meetings:index")
    context = {
        "form": form,
        "to_user": to_user,
    }
    return render(request, "notes/send.html", context)


def detail(request, pk):
    note = get_object_or_404(Notes, pk=pk)

    if request.user == note.from_user:
      return render(request, "notes/detail.html", {"note": note})

    if request.user == note.to_user:
        if not note.read:
            note.read = True
            note.save()
        return render(request, "notes/detail.html", {"note": note})
    else:
        messages.error(request, "그렇게는 볼 수 없어요.😅")
        return redirect("notes:index")


def delete(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    print(request.POST)
    if request.user == note.to_user and request.method == "POST":
        note.delete()
        return JsonResponse({"pk": pk})
    else:
        messages.error(request, "남의 쪽지는 지울 수 없어요.😅")
        return redirect("notes:index")
