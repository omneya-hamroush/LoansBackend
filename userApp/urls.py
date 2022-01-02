from django.urls import path, include

from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from userApp import views


router = DefaultRouter()

urlpatterns = [
    url(r'^users/login/$', views.LoginViewSet.as_view()),
    url(r'^users/logout/$', views.LogoutView.as_view()),
]
