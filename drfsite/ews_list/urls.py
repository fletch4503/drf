from django.urls import (
    path,
    re_path,
    include,
)

from . import views

app_name = "ews_list"

urlpatterns = [
    path("", views.index_view, name="index"),
]