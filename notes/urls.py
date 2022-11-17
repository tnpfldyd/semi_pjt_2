from . import views
from django.urls import path

app_name = "notes"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/send/", views.send, name="send"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
