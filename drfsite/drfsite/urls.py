"""
URL configuration for drfsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from ews_list.views import *
from women.views import *

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),  # Class-based views
    path("about/", TemplateView.as_view(template_name="about.html"), name="About"),
    path('admin/', admin.site.urls),
    path('women/', include("women.urls")),
    path("ews/", include("ews_list.urls")),  # Including EWS URLconf
    # path('api/v1/womenlist/', WomenAPIView.as_view()),
    path('api/v1/womenlist/', WomenAPIList.as_view()),
    path('api/v1/ewslist/', ewsAPIList.as_view()),
    # path('api/v1/womenlist/<int:pk>/', WomenAPIView.as_view()),
]
