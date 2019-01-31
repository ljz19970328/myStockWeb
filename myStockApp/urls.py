from django.conf.urls import url
from myStockApp import views

app_name = 'myStockApp'   # url反向解析

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^index/', views.index),
    url(r'^verify_code/$', views.verify_code),
]