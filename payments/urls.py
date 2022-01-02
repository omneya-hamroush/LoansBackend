from django.urls import path, include

from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from payments import views


router = DefaultRouter()


urlpatterns = [
    path('',include(router.urls)),
    url(r'^getpayments', views.GetPayments.as_view()),
    url(r'^addpayment', views.AddPayment.as_view()),
    url(r'^approvefund', views.ApproveFund.as_view()),
    ]
