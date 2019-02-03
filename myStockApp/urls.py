from django.conf.urls import url
from myStockApp import views
from myStockApp import dealStockdata

app_name = 'myStockApp'   # url反向解析

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^index/', views.index),
    url(r'^verify_code/$', views.verify_code),


    url(r'^search/', dealStockdata.search),
    url(r'^show_searchResult/', dealStockdata.show_searchResult),
    url(r'^main/', dealStockdata.main),
]