from . import views
from django.urls import path

app_name = "shoppings"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:num>/", views.search, name="search"),
]
