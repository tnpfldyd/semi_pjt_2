from multiprocessing import AuthenticationError
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from django.http import JsonResponse
from cards.models import *
from django.db.models import *
import datetime

# Create your views here.
def signup(request):
    gender = request.POST.get("gender")
    age = request.POST.get("age")
    print(gender, age)
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.gender = gender
            forms.age = age
            forms.save()
            return redirect("accounts:index")
    else:
        form = SignupForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def index(request):
    return render(request, "accounts/index.html")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


import secrets, os

state_token = secrets.token_urlsafe(16)


def kakao_request(request):
    kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    redirect_uri = "http://localhost:8000/accounts/kakao/login/callback/"
    client_id = os.getenv("KAKAO_ID")
    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


def kakao_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("KAKAO_ID"),
        "redirect_uri": "http://localhost:8000/accounts/kakao/login/callback/",
        "code": request.GET.get("code"),
        "client_secret": os.getenv("KAKAO_SECRET"),
    }
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    temp = requests.post(kakao_token_api, data=data).json()
    access_token = temp["access_token"]

    headers = {"Authorization": f"bearer ${access_token}"}
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    kakao_user_information = requests.get(kakao_user_api, headers=headers).json()
    kakao_id = kakao_user_information["id"]
    kakao_nickname = kakao_user_information["properties"]["nickname"]
    kakao_profile_image = kakao_user_information["properties"]["profile_image"]
    kakao_email = kakao_user_information["kakao_account"].get("email")
    kakao_age_range = kakao_user_information["kakao_account"].get("age_range")
    kakao_gender = kakao_user_information["kakao_account"].get("gender")

    if get_user_model().objects.filter(username=kakao_id).exists():
        kakao_user = get_user_model().objects.get(username=kakao_id)
        kakao_user.refresh_token = temp["refresh_token"]
        kakao_user.profileimage = kakao_profile_image
        kakao_user.save()
    else:
        kakao_login_user = get_user_model().objects.create(
            username=kakao_id,
            nickname=kakao_nickname,
            profileimage=kakao_profile_image,
            email=kakao_email,
            age_range=kakao_age_range,
            gender=kakao_gender,
            refresh_token=temp["refresh_token"],
        )
        kakao_login_user.set_password(str(state_token))
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(username=kakao_id)
    auth_login(request, kakao_user, backend="django.contrib.auth.backends.ModelBackend")
    if request.user.blockers.count() > 9:
        auth_logout(request)
        messages.error(request, "누적 신고 횟수가 많아 로그인 할 수 없어요.😥")
    else:
        messages.success(request, "오신걸 환영합니다.😀")
    return redirect(request.GET.get("next") or "accounts:index")


@login_required
def mypage(request):
    block_users = request.user.blocking.all()
    block_cnt = len(block_users)
    return render(
        request,
        "accounts/mypage.html",
        {"user": get_user_model().objects.get(pk=request.user.pk), "block_users": block_users, "block_cnt": block_cnt,},
    )


def logout(request):
    auth_logout(request)
    return redirect("accounts:index")


def update(request):
    if request.method == "POST":
        print(request.POST, request.FILES)
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.age_range = temp.age_range[-2:-1] + "0~" + temp.age_range[-2:-1] + "9"
            temp.save()
            return redirect("accounts:index")
    else:
        form = UpdateForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


import requests


def delete(request):
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("KAKAO_ID"),
        "refresh_token": request.user.refresh_token,
        "client_secret": os.getenv("KAKAO_SECRET"),
    }

    response = requests.post(url, data=data).json()
    access_token = response["access_token"]
    url = "https://kapi.kakao.com/v1/user/unlink"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer ${access_token}",
    }
    response = requests.post(url, headers=headers)
    request.user.delete()
    auth_logout(request)
    return redirect("accounts:index")


@login_required
def follow(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk)
    if person != request.user and request.method == "POST":
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_follow = False
        else:
            person.followers.add(request.user)
            is_follow = True
        context = {
            "isFollow": is_follow,
            "followersCount": person.followers.count(),
            "followingsCount": person.followings.count(),
        }
        return JsonResponse(context)
    else:
        messages.warning(request, "그건 안됨.")
        return redirect("meetings:index")


@login_required
def block(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk)
    if person != request.user and request.method == "POST":
        if person.blockers.filter(pk=request.user.pk).exists():
            person.blockers.remove(request.user)
            is_follow = False
            messages.success(request, "차단이 해제되었습니다.")
        else:
            person.blockers.add(request.user)
            is_follow = True
            messages.success(request, "차단 되었습니다.")
        context = {
            "isFollow": is_follow,
        }
        return JsonResponse(context)
    else:
        messages.warning(request, "그건 안됨.")
        return redirect("meetings:index")



def profile(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def save(request):
    if request.method == "POST":
        tree_notice = request.GET.get("p")
        note_notice = request.GET.get("h6")
        if tree_notice == "ON":
            request.user.tree_notice = True
        else:
            request.user.tree_notice = False
        if note_notice == "ON":
            request.user.note_notice = True
        else:
            request.user.note_notice = False
        request.user.save()
        messages.success(request, "저장 성공.😀")
        return JsonResponse({1: 1})
    else:
        messages.error(request, "그렇게는 접근할 수 없어요.😥")
        return redirect("accounts:mypage")


@login_required
def notice(request):
    if request.method == "POST":
        dic = {}
        if request.user.tree_notice:
            if request.user.usercard:
                card = request.user.usercard
                false_comments = card.usercomment_set.filter(read=False)
                for i in false_comments:
                    if i.created_at not in dic:
                        dic[i.created_at.strftime("%Y-%m-%dT%H:%M:%S")] = (
                            i.content,
                            i.user.nickname,
                            "card",
                            card.pk,
                        )
                    else:
                        dic[
                            (i.created_at + datetime.timedelta(minutes=1)).strftime(
                                "%Y-%m-%dT%H:%M:%S"
                            )
                        ] = (
                            i.content,
                            i.user.nickname,
                            "card",
                            card.pk,
                        )
        if request.user.note_notice:
            if request.user.user_to.filter(read=False).exists():
                false_notes = request.user.user_to.filter(read=False)
                for i in false_notes:
                    if i.created_at not in dic:
                        dic[i.created_at.strftime("%Y-%m-%dT%H:%M:%S")] = (
                            i.title,
                            i.from_user.nickname,
                            "note",
                            i.pk,
                        )
                    else:
                        dic[
                            (i.created_at + datetime.timedelta(minutes=1)).strftime(
                                "%Y-%m-%dT%H:%M:%S"
                            )
                        ] = (i.title, i.from_user.nickname, "note", i.pk)
        dic = sorted(dic.items(), reverse=True)
        print(dic)
        return JsonResponse({"items": dic})
    else:
        messages.error(request, "그렇게는 접근할 수 없어요.😥")
        return redirect("meetings:index")
