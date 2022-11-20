from django.urls import path
from . import views

app_name = "cards"

urlpatterns = [
    path("", views.index, name="index"),
    # 개인카드
    path("create/indiv/", views.usercard_create, name="usercard_create"),
    path("create/indiv/2", views.usercard_create2, name="usercard_create2"),
    path("detail/usercard/<int:pk>/", views.usercard_detail, name="usercard_detail"),
    path("<int:pk>/usercard/update/", views.usercard_update, name="usercard_update"),
    path("<int:pk>/usercard/update/2", views.usercard_update2, name="usercard_update2"),
    path("usercard/delete/", views.usercard_delete, name="usercard_delete"),
    path(
        "<int:pk>/usercard/comments/", views.usercard_comment, name="usercard_comment"
    ),
    path(
        "<int:pk>/usercard/comments/2",
        views.usercard_comment2,
        name="usercard_comment2",
    ),
    # 그룹카드
    path("create/group/", views.group_create, name="group_create"),
    path("<int:pk>/create/group/2", views.group_create2, name="group_create2"),
    path("detail/group/<int:pk>/", views.group_detail, name="group_detail"),
    path("<int:pk>/group/update/", views.groupcard_update, name="groupcard_update"),
    path("<int:pk>/group/delete/", views.groupcard_delete, name="groupcard_delete"),
    path("<int:pk>/gcomments/", views.gcomment_create, name="gcomment_create"),
    path("search/", views.search, name="search"),
    # path(
    #     "<int:cards_pk>/group/<int:comment_pk>/delete/",
    #     views.gcomments_delete,
    #     name="gcomments_delete",
    # ),
]
