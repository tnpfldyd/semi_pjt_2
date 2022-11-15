from django.urls import path
from . import views

app_name = "cards"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/indiv/", views.create_indiv, name="create_indiv"),
    path("create/group/", views.create_group, name="create_group"),
    path("<int:pk>/", views.group_detail, name="group_detail"),
    path("detail/indiv/", views.indiv_detail, name="indiv_detail"),
    path("<int:pk>/update/", views.card_update, name="card_update"),
    path("delete/", views.card_delete, name="card_delete"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
]
