from django.urls import path, re_path, include
# from django.views.generic import TemplateView

from . import views

app_name = "women"
actress_patterns = [
    path("", views.actress),
    path("comments", views.comments),
    path("top", views.top),
]

urlpatterns = [
    path("", views.WomenListIndexView.as_view(), name="index"),
    path("list/", views.WomenListView.as_view(), name="list"),  # Список всех женщин - отображение на основе класса
    path("<int:pk>/", views.WomenDetailView.as_view(), name="detail"),  # Детальный вид по элементу из списка
    re_path(r'about', views.about, name="about"),
    path("actress/", include(actress_patterns)),
    path("add/", views.CreateWomenView.as_view(), name="add"),
    # path("add/", views.postwoman, name="add"),

]
