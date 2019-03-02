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
    url(r'^logout/', views.logout),
    url(r'^perAdd/', views.perAdd),
    url(r'^loginCheck/', views.loginCheck),
    url(r'^callMaster/', views.callMaster),
    url(r'^personCenter/', views.personCenter),
    url(r'^collection_stock/', views.collection_Stock),
    url(r'^del_stockDetails/', views.del_collection_Stock),

    url(r'^main/', dealStockdata.main),
    url(r'^search/', dealStockdata.search),
    url(r'^show_searchResult/', dealStockdata.show_searchResult),
    url(r'^query_stockDetails/', dealStockdata.query_stockDetails),
    url(r'^show_stockDetails/', dealStockdata.show_stockDetails),
    url(r'^collection_stockDetails/', dealStockdata.show_collection_stockDetails),
    url(r'^get_sort/', dealStockdata.stock_fluctuation),
    url(r'^get_index/', dealStockdata.get_index),
    url(r'^get_index_line_chart/', dealStockdata.get_index_line_chart),
    url(r'^news/', dealNews.show_news),
    url(r'^get_news/', dealNews.get_news),
    url(r'^get_sina_news/', dealNews.main_show_sina_news),
]