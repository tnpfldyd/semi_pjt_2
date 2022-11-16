from django.urls import path
from . import views

app_name = "vocies"

urlpatterns = [
    path("", views.index, name="index"),
    path("myvocie/", views.myvocie, name="myvocie"),
    path("create/", views.create, name="create"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/comment/", views.comment, name="comment"),
    path("manage_page/", views.manage_page, name="manage_page"),
]
