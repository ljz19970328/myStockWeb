from django.conf.urls import url
from myStockApp import views, dealSearch, dealEmail
from myStockApp import dealCollection
from myStockApp import dealStockData
from myStockApp import dealNews

app_name = 'myStockApp'  # url反向解析

urlpatterns = [
    #  配置views.py的映射
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^index/', views.index),
    url(r'^verify_code/$', views.verify_code),
    url(r'^logout/', views.logout),
    url(r'^perAdd/', views.show_person_info),
    url(r'^loginCheck/', views.loginCheck),
    url(r'^personCenter/', views.personCenter),
    #  配置dealCollection.py的映射
    url(r'^collection_stock/', dealCollection.collection_Stock),
    url(r'^del_stockDetails/', dealCollection.del_collection_Stock),
    url(r'^show_myCollection/', dealCollection.show_myCollection),
    url(r'^collection_stockDetails/', dealCollection.show_collection_stockDetails),
    #  配置dealStockData.py的映射
    url(r'^main/', dealStockData.main),
    url(r'^query_stockDetails/', dealStockData.query_stockDetails),
    url(r'^show_stockDetails/', dealStockData.show_stockDetails),
    url(r'^logo/', dealStockData.companyLogo_image),
    url(r'^get_sort/', dealStockData.stock_fluctuation),
    url(r'^get_index/', dealStockData.get_index),
    url(r'^get_index_line_chart/', dealStockData.get_index_line_chart),
    #  配置dealSearch.py的映射
    url(r'^search/', dealSearch.search),
    url(r'^show_searchResult/', dealSearch.show_searchResult),
    #  配置dealNews.py的映射
    url(r'^news/', dealNews.show_news),
    url(r'^get_news/', dealNews.get_news),
    url(r'^get_sina_news/', dealNews.main_show_sina_news),
    #  配置dealEmail.py的映射
    url(r'^callMaster/', dealEmail.callMaster),
]
