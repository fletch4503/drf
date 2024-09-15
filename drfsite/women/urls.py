from django.urls import path, re_path
# from django.views.generic import TemplateView

from . import views

app_name = "women"

urlpatterns = [
    path("", views.women_index, name="index"),
]