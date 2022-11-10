from . import views
from django.urls import path

app_name = "meetings"

path("", views.index, name="index"),
path("create/", views.create, name="create"),
path("<int:meeting_pk>/", views.detail, name="detail"),
path("<int:meeting_pk>/update", views.update, name="update"),
path("<int:meeting_pk>/delete", views.delete, name="delete"),