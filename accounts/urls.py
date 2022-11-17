from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("kakao/login/callback/", views.kakao_callback, name="kakao_callback"),
    path("login/kakao/", views.kakao_request, name="kakao"),
    path("mypage/", views.mypage, name="mypage"),
    path("update/", views.update, name="update"),
    path("delete/", views.delete, name="delete"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("<int:pk>/block/", views.block, name="block"),
    path("block_user/", views.block_user, name="block_user"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    # path("profile/<str:username>/", views.profile, name="profile"),
    path("save/", views.save, name="save"),
    path("notice/", views.notice, name="notice"),
]
