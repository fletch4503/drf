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
    # path("<pk>/", views.ewsitemDetailView.as_view()),
    path("<int:pk>/", views.ewsitemDetailView.as_view(), name="detail"),
    # path("<int:pk>/", views.ewsitemDetailView.as_view(), name="detail"),
    path("list/", views.ewsitemList.as_view(), name="list"),
    # path("add/", views.ewsitemCreate.as_view(), name="add"),
    path("add/", views.ewsitemFormView.as_view(), name="add"),
    # path("add/", views.ewsitemFormView.as_view(success_url="/"), name="add"),
    # path('<slug:slug>/', views.ewsitemDetailView.as_view(), name="detail"),
    re_path(r'about', views.about, name="about"),
    # path("actress/", include(actress_patterns)),

]
