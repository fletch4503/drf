from django.urls import (
    path,
    re_path
)

from . import views

app_name = "ews_list"
# actress_patterns = [
#     path("", views.actress),
#     path("comments", views.comments),
#     path("top", views.top),
# ]

urlpatterns = [
    path("", views.ewsitemListIndexView.as_view(), name="index"),
    path("<int:pk>/", views.ewsitemDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.ewsitemUpdateView.as_view(), name="update"),
    path("<int:pk>/confirm-delete/", views.ewsitemDeleteView.as_view(), name="delete"),
    path("list/", views.ewsitemList.as_view(), name="list"),
    path("add/", views.ewsitemCreateView.as_view(), name="add"),
    # path("list/", views.ToDoListView.as_view(), name="list"),
    # path("done/", views.ToDoListDoneView.as_view(), name="done"),
    # path("create/", views.ToDoItemCreateView.as_view(), name="create"),
    re_path(r'about', views.about, name="about"),

]
