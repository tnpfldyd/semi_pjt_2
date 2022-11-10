from django.urls import path
from . import views

app_name = "cards"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/indiv/", views.createindiv, name="createindiv"),
    path("create/group/", views.creategroup, name="creategroup"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
]
