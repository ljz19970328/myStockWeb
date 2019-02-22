from django.conf.urls import url
from myStockApp import views
from myStockApp import dealStockdata


app_name = 'myStockApp'   # url反向解析

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^perAdd/', views.perAdd),
    url(r'^loginCheck/', views.loginCheck),
    url(r'^callMaster/', views.callMaster),
    url(r'^personCenter/', views.personCenter),


    url(r'^main/', dealStockdata.main),
    url(r'^search/', dealStockdata.search),
    url(r'^show_searchResult/', dealStockdata.show_searchResult),
    url(r'^query_stockDetails/', dealStockdata.query_stockDetails),
    url(r'^show_stockDetails/', dealStockdata.show_stockDetails),
]