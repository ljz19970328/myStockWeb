import time
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
import json
from myStockApp.models import Stock
from myStockApp.models import StockDetails
import tushare as ts
from django.db.models import Q
token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


def search(request):
    stock_info = request.POST.get('stock_info')
    response = {"msg": ""}
    try:
        global stock_data
        stock_data = Stock.objects.filter(Q(ts_code=stock_info) | Q(symbol=stock_info) | Q(name=stock_info) |
                                     Q(area=stock_info) |Q(industry=stock_info) | Q(market=stock_info))
        response['msg'] = 'ok'
    except:
        response['msg'] = 'flase'
        print("查询失败")
    return JsonResponse(response)


def show_searchResult(request):
    return render(request, 'searchResults.html',{'searchResults': stock_data})


def query_stockDetails(request):
    ts_code = request.POST.get('ts_code')
    request.session['global_ts_code'] = ts_code
    global stock_details
    stock_details = StockDetails.objects.filter(ts_code=ts_code)
    response = {"msg": ""}
    return JsonResponse(response)


# 获得股票基本面数据 交易日每日15点～17点之间更新
def del_daily_basic(ts_code):
    trade_date = time.strftime('%Y%m%d', time.localtime(time.time()-86400))
    df = pro.daily_basic(ts_code=ts_code, trade_date=trade_date)
    data = df.to_json(orient='index')  # dataframe转json
    temp_data = json.loads(data)  # json转dict
    daily_basic_data = temp_data['0']  # dic 取第一条记录
    class dicToObj:  # dict转obj
        def __init__(self, **entries):
            self.__dict__.update(entries)
    r = dicToObj(**daily_basic_data)
    return daily_basic_data


# 获得日线数据，提取日k线所需数据，交易日每天15点～16点之间更新
def deal_Daily(ts_code):
    df = pro.daily(ts_code=ts_code, start_date='20180101')
    trade_date = df["trade_date"]
    k_line_data = df[["open", "close", "low", "high"]]
    temp_data = trade_date.tolist()
    categoryData=list(reversed(temp_data))
    temp_data = np.array(k_line_data)
    values = temp_data.tolist()
    values=list(reversed(values))
    return (categoryData,values)


# 获得周线数据，提取周k线所需数据
def deal_Weekly(ts_code):
    df = pro.weekly(ts_code=ts_code, start_date='20160101')
    trade_date = df["trade_date"]
    k_line_data = df[["open", "close", "low", "high"]]
    temp_data = trade_date.tolist()
    categoryData = list(reversed(temp_data))
    temp_data = np.array(k_line_data)
    values = temp_data.tolist()
    values = list(reversed(values))
    return (categoryData, values)


# 获得月线数据，提取月k线所需数据
def deal_Monthly(ts_code):
    df = pro.monthly(ts_code=ts_code, start_date='20140101')
    trade_date = df["trade_date"]
    k_line_data = df[["open", "close", "low", "high"]]
    temp_data = trade_date.tolist()
    categoryData = list(reversed(temp_data))
    temp_data = np.array(k_line_data)
    values = temp_data.tolist()
    values = list(reversed(values))
    return (categoryData, values)


def show_stockDetails(request):
    stockDetails=stock_details
    ts_code = request.session.get('global_ts_code')

    categoryData0, values0 = deal_Daily(ts_code)
    categoryData1, values1 = deal_Weekly(ts_code)
    categoryData2, values2 = deal_Monthly(ts_code)
    daily_basic_data = del_daily_basic(ts_code)
    return render(request, 'stockDetails.html', locals())


def main(request):
    return render(request,"main.html")


