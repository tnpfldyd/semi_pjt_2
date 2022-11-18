from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Meeting
from .forms import MeetingForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import json
import random

# Create your views here.


def home(request):
    return render(request, "meetings/home.html")


def index(request):
    meetings = Meeting.objects.order_by("-pk")
    meetings_all = Meeting.objects.all()

    img = ["https://images.unsplash.com/photo-1482517967863-00e15c9b44be?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80", "https://images.unsplash.com/photo-1615097130643-12caeab3c625?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80" , "https://images.unsplash.com/photo-1577042939454-8b29d442b402?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80" , "https://images.unsplash.com/photo-1638277267253-543e4c57cd7f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"]
    s = random.choice(img)
    
    # 모임이 몇개 개설됐는지
    meetings_count = Meeting.objects.all().count()

    # 지역별
    meetings_local = meetings_all
    meetings_local_name = "모든지역"
    meetings_local_list = ["노원구", "송파구"]

    nw = "노원구"
    sp = "송파구"

    at_all = "모두보기"
    paginator = Paginator(meetings, 4)
    page_number = request.GET.get("local")
    page_obj = paginator.get_page(page_number)

    if request.POST.get("reset"):
        return redirect("meetings:index")

    if request.GET.get("local") and nw in request.GET.get("local"):

        meetings_local = Meeting.objects.filter(location__contains=nw).order_by("-pk")
        meetings_local_name = nw
        # 페이지네이션
        paginator = Paginator(meetings_local, 4)
        page_number = request.GET.get("local")  # key 값이 local, value 값이 노원구
        page_number = page_number.strip(nw)  # 노원구2 에서 노원구를 제거
        page_obj = paginator.get_page(page_number)  # 숫자만 받음

        context = {
            "s": s,
            "nw": nw,
            "meetings": meetings,
            "meetings_all": meetings_all,
            "page_obj": page_obj,
            "meetings_local": meetings_local,
            "meetings_local_name": meetings_local_name,
            "meetings_count": meetings_count,
            "meetings_local_list": meetings_local_list,
        }

        return render(request, "meetings/index.html", context)

    elif request.GET.get("local") and sp in request.GET.get("local"):
        meetings_local = Meeting.objects.filter(location__contains=sp).order_by("-pk")
        meetings_local_name = sp
        # 페이지네이션
        paginator = Paginator(meetings_local, 4)
        page_number = request.GET.get("local")
        page_number = page_number.strip(sp)
        page_obj = paginator.get_page(page_number)

        context = {
            "s": s,
            "sp": sp,
            "meetings": meetings,
            "page_obj": page_obj,
            "meetings_all": meetings_all,
            "meetings_local": meetings_local,
            "meetings_local_name": meetings_local_name,
            "meetings_count": meetings_count,
            "meetings_local_list": meetings_local_list,
        }

        return render(request, "meetings/index.html", context)

    else:

        context = {
            "s": s,
            "at_all": at_all,
            "meetings": meetings,
            "page_obj": page_obj,
            "meetings_all": meetings_all,
            "meetings_local": meetings_local,
            "meetings_local_name": meetings_local_name,
            "meetings_count": meetings_count,
            "meetings_local_list": meetings_local_list,
        }
        return render(request, "meetings/index.html", context)


dic = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}






def create(request):
    if request.method == "POST":
        meeting_form = MeetingForm(request.POST, request.FILES)
        # b = MeetingForm(auto_id=False)
        # print(b)
        if meeting_form.is_valid():
            meeting = meeting_form.save(commit=False)
            meeting.user = request.user
            meeting.save()

            temp = ""
            
            for i in str(meeting.pk):
                temp += dic[i]
            meeting.text = temp
            meeting.save()
            return redirect("meetings:index")
    else:
        meeting_form = MeetingForm()

    context = {
        "meeting_form": meeting_form,
    }

    return render(request, "meetings/create.html", context)


def password(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    print(meeting.password)
    print(request.POST.get("password"))
    if request.POST.get("password") == meeting.password:

        return detail(request, meeting_pk)
    else:
        messages.warning(request, "비밀번호가 일치하지 않습니다.😀")
        return redirect("meetings:index")


def detail(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    comments = meeting.comment_set.all()
    form = CommentForm()

    user_list = meeting.belong.all()  # 유저리스트를 보여줄 코드

    user = request.user # request.user => 현재 로그인한 유저
    if meeting.belong.filter(id = user.id).exists() == False:
      messages.success(request, "참여를 누르면 비밀번호 없이 입장할 수 있습니다.😀")

    if request.POST.get("belong_id2"):
        if meeting.belong.filter(id=user.id).exists():  # 이미 참여를 누른 유저일 때
            meeting.belong.remove(user)
            messages.error(request, "참여 취소😀")
        else:  # 참여를 누르지 않은 유저일 때
            meeting.belong.add(user)  # belong 필드에 현재 유저 삭제
            messages.success(request, "참여 성공😀")
        return redirect("meetings:index")

    if request.POST.get("belong_id"):
        if meeting.belong.filter(id=user.id).exists():  # 이미 참여를 누른 유저일 때
            meeting.belong.remove(user)
            messages.error(request, "참여 취소😀")
        else:  # 참여를 누르지 않은 유저일 때
            meeting.belong.add(user)  # belong 필드에 현재 유저 삭제
            messages.success(request, "참여 성공😀")

    # DB에 존재하면 바로 입장.

    if meeting.belong.filter(id=user.id).exists():

        context = {
            "user_list": user_list,
            "meeting": meeting,
            "comments": comments,
            "commentform": form,
        }
        return render(request, "meetings/detail.html", context)

    else:
        context = {
            "user_list": user_list,
            "meeting": meeting,
            "comments": comments,
            "commentform": form,
        }
        return render(request, "meetings/detail.html", context)


def update(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    if request.user == meeting.user:
        if request.method == "POST":
            meeting_form = MeetingForm(request.POST, request.FILES, instance=meeting)
            if meeting_form.is_valid():
                meeting_form.save()
                return redirect("meetings:detail", meeting.pk)
        else:
            meeting_form = MeetingForm(instance=meeting)
        context = {
            "meeting_form": meeting_form,
        }
        return render(request, "meetings/update.html", context)
    else:
        return redirect("meetings:detail", meeting.pk)


def delete(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    if request.user == meeting.user:
        meeting.delete()
        return redirect("meetings:index")


def comment_create(request, meeting_pk):
    meeting_data = Meeting.objects.get(pk=meeting_pk)

    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        print("여기?!")
        if form.is_valid():
            print("여긴되나?")
            comment = form.save(commit=False)
            comment.meeting = meeting_data
            comment.user = request.user
            comment.save()

        return redirect("meetings:detail", meeting_pk)
    else:
        return redirect("accounts:login")


def comment_delete(request, meeting_pk, comment_pk):
    meeting_data = Meeting.objects.get(pk=meeting_pk)
    comment_data = meeting_data.comment_set.get(pk=comment_pk)

    if request.user == comment_data.user:
        comment_data.delete()

    return redirect("meetings:detail", meeting_pk)


def belong_meeting(request, pk):
    meeting = Meeting.objects.get(pk=pk)

    if request.user in meeting.belong_meeting.all():
        meeting.belong_meeting.remove(request.user)
    else:
        meeting.belong_meeting.add(request.user)

    return redirect("meetings:detail", pk)
