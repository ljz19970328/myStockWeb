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


    url(r'^main/', dealStockdata.main),
    url(r'^search/', dealStockdata.search),
    url(r'^show_searchResult/', dealStockdata.show_searchResult),
    url(r'^query_stockDetails/', dealStockdata.query_stockDetails),
    url(r'^show_stockDetails/', dealStockdata.show_stockDetails),
    url(r'^show_daily_line/', dealStockdata.deal_Daily),
    url(r'^show_Weekly_line/', dealStockdata.deal_Monthly),
    url(r'^show_Monthly_line/', dealStockdata.deal_Weekly)
]