from . import views
from django.urls import path

app_name = "shoppings"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("<str:string>/sort/", views.ssort, name="sort"),
]
