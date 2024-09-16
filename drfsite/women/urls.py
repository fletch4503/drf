from django.urls import path, re_path
# from django.views.generic import TemplateView

from . import views

app_name = "women"

urlpatterns = [
    path("", views.WomenListIndexView.as_view(), name="index"),
    path("list/", views.WomenListView.as_view(), name="list"),  # Список всех женщин - отображение на основе класса
    path("<int:pk>/", views.WomenDetailView.as_view(), name="detail"),  # Детальный вид по элементу из списка

]
