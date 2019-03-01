from django.conf.urls import url
from myStockApp import views
from myStockApp import dealStockdata
from myStockApp import dealNews


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
    url(r'^get_sort/', dealStockdata.stock_fluctuation),
    url(r'^news/', dealNews.show_news),
    url(r'^get_news/', dealNews.get_news),
]