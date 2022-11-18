from . import views
from django.urls import path

app_name = "meetings"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:meeting_pk>/", views.detail, name="detail"),
    path("<int:meeting_pk>/update/", views.update, name="update"),
    path("<int:meeting_pk>/delete/", views.delete, name="delete"),
    path(
        "<int:meeting_pk>/comment/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("<int:meeting_pk>/password/", views.password, name="password"),
    # comment
    path("<int:meeting_pk>/comment/create/", views.comment_create, name="comment_create"),
]
