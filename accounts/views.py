from multiprocessing import AuthenticationError
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages

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
    print(kakao_user_information)

    if get_user_model().objects.filter(username=kakao_id).exists():
        kakao_user = get_user_model().objects.get(username=kakao_id)
    else:
        kakao_login_user = get_user_model().objects.create(
            username=kakao_id,
            nickname=kakao_nickname,
            profileimage=kakao_profile_image,
            email=kakao_email,
            age_range=kakao_age_range,
            gender=kakao_gender,
        )
        kakao_login_user.set_password(str(state_token))
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(username=kakao_id)
    auth_login(request, kakao_user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect(request.GET.get("next") or "accounts:index")


@login_required
def mypage(request):
    return render(
        request, "accounts/mypage.html", {"user": get_user_model().objects.get(pk=request.user.pk)}
    )
