from django.urls import path
from . import views

app_name = "cards"

urlpatterns = [
    path("", views.index, name="index"),
    # 개인카드
    path("create/indiv/", views.usercard_create, name="usercard_create"),
    path("detail/usercard/<int:pk>/", views.usercard_detail, name="usercard_detail"),
    path("<int:pk>/usercard/update/", views.usercard_update, name="usercard_update"),
    path("usercard/delete/", views.usercard_delete, name="usercard_delete"),
    path(
        "<int:pk>/usercard/comments/", views.usercard_comment, name="usercard_comment"
    ),
    # 그룹카드
    path("create/group/", views.group_create, name="group_create"),
    path("detail/group/<int:pk>/", views.group_detail, name="group_detail"),
    path("<int:pk>/group/update/", views.groupcard_update, name="groupcard_update"),
    path("<int:pk>/group/delete/", views.groupcard_delete, name="groupcard_delete"),
    path("<int:pk>/gcomments/", views.gcomment_create, name="gcomment_create"),
    # path(
    #     "<int:cards_pk>/group/<int:comment_pk>/delete/",
    #     views.gcomments_delete,
    #     name="gcomments_delete",
    # ),
]
