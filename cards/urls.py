from django.urls import path
from . import views

app_name = "cards"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/indiv/", views.create_indiv, name="create_indiv"),
    path("create/group/", views.create_group, name="create_group"),
    # 주소 정리해야함
    path("<int:pk>/", views.group_detail, name="group_detail"),
    path("detail/indiv/", views.indiv_detail, name="indiv_detail"),
    path("<int:pk>/update/", views.card_update, name="card_update"),
    path("delete/", views.card_delete, name="card_delete"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path("<int:pk>/usercard/update/", views.usercard_update, name="usercard_update"),
    path("usercard/delete/", views.usercard_delete, name="usercard_delete"),
    path(
        "<int:pk>/usercard/comments/", views.usercard_comment, name="usercard_comment"
    ),
]
