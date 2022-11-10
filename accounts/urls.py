from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("login/kakao/", views.kakao_request, name="kakao"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao_callback"),
]
