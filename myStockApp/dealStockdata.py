import time
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
import json

from pandas import DataFrame

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


# stock涨跌序列排序
def stock_fluctuation():
    trade_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.daily(trade_date='20190215')
    data = df[['ts_code', 'pre_close', 'open', 'close', 'pct_chg']]
    data = data.to_json(orient='index')
    temp_data = json.loads(data)
    stockList = []
    for i in temp_data:
        # dict转obj
        class DicToObj:
            def __init__(self, **entries):
                self.__dict__.update(entries)

        r = DicToObj(**temp_data[i])
        stockList.append(r)

    # ！！！！快排算法！！！！
    def part(List, begin, end):
        k = List[end].pct_chg
        i = begin - 1
        for j in range(begin, end):
            if List[j].pct_chg <= k:
                i += 1
                List[j], List[i] = List[i], List[j]
        List[end], List[i + 1] = List[i + 1], List[end]
        return i + 1

    def quickSort(List, left, right):
        if left < right:
            mid = part(List, left, right)
            quickSort(List, left, mid - 1)
            quickSort(List, mid + 1, right)

    quickSort(stockList, 0, len(stockList) - 1)
    # ！！！！快排算法！！！！


def query_stockDetails(request):
    ts_code = request.POST.get('ts_code')
    request.session['global_ts_code'] = ts_code
    global stock_details
    stock_details = StockDetails.objects.filter(ts_code=ts_code)
    response = {"msg": ""}
    return JsonResponse(response)


# 获得股票基本面数据 交易日每日15点～17点之间更新
def del_daily_basic(ts_code):
    stamp = time.time()  # 获取当前时间戳
    date = time.localtime(stamp)  # 利用localtime()转换为时间数组
    hour = int(time.strftime('%H', date))
    if hour > 15:
        # 时间戳为当天
        trade_date = time.strftime('%Y%m%d', date)  # 没有跟新的话时间戳减一天
    elif hour <= 15:
        # 时间戳为前一天
        trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400))  # 没有跟新的话时间戳减一天
    df = pro.daily_basic(ts_code=ts_code, trade_date=trade_date)
    data = df.to_json(orient='index')  # dataframe转json
    temp_data = json.loads(data)  # json转dict
    daily_basic_data = temp_data['0']  # dic 取第一条记录

    # dict转obj
    class DicToObj:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    r = DicToObj(**daily_basic_data)
    return daily_basic_data


# 获得日线数据，提取日k线所需数据，交易日每天15点～16点之间更新
def deal_Daily(ts_code):
    df = pro.daily(ts_code=ts_code, start_date='20180101')
    trade_date = df["trade_date"]
    k_line_data = df[["open", "close", "low", "high"]]
    vol = df["vol"]
    # 获得时间序列
    temp_data = trade_date.tolist()
    categoryData = list(reversed(temp_data))
    # 获得k线数据序列
    temp_data = np.array(k_line_data)
    values = temp_data.tolist()
    values = list(reversed(values))
    # 获得成交量序列
    temp_data = vol.tolist()
    volume = list(reversed(temp_data))
    macd, dea, diff = cal_macd(df, ts_code, '20180101')
    # 返回值
    return (categoryData,values,volume,macd,dea,diff)


# 获得周线数据，提取周k线所需数据
def deal_Weekly(ts_code):
    df = pro.weekly(ts_code=ts_code, start_date='20130101')
    trade_date = df["trade_date"]
    k_line_data = df[["open", "close", "low", "high"]]
    vol = df["vol"]
    # 获得时间序列
    temp_data = trade_date.tolist()
    categoryData = list(reversed(temp_data))
    # 获得k线数据序列
    temp_data = np.array(k_line_data)
    values = temp_data.tolist()
    values = list(reversed(values))
    # 获得成交量序列
    temp_data = vol.tolist()
    volume = list(reversed(temp_data))
    macd, dea, diff = cal_macd(df, ts_code, '20160101')
    # 返回值
    return(categoryData, values, volume,macd,dea,diff)


# 获得月线数据，提取月k线所需数据
def deal_Monthly(ts_code):
    df = pro.monthly(ts_code=ts_code, start_date='19910101')
    trade_date = df["trade_date"]
    k_line_data = df[["open", "close", "low", "high"]]
    vol = df["vol"]
    # 获得时间序列
    temp_data = trade_date.tolist()
    categoryData = list(reversed(temp_data))
    # 获得k线数据序列
    temp_data = np.array(k_line_data)
    values = temp_data.tolist()
    values = list(reversed(values))
    # 获得成交量序列
    temp_data = vol.tolist()
    volume = list(reversed(temp_data))
    macd, dea, diff = cal_macd(df, ts_code, '20000101')
    # 返回值
    return (categoryData, values, volume, macd, dea, diff)


def cal_macd(data,ts_code,start_data):

    # data是包含高开低收成交量的标准dataframe
    # short_,long_,m分别是macd的三个参数
    # 返回值是diff,dea,macd三个list

    short_ = 12
    long_ = 26
    m = 9
    data = data.reindex(index=data.index[::-1])
    data['diff'] = data['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                data['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
    data['dea'] = data['diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
    data['macd'] = 2*(data['diff']-data['dea'])
    # 获得macd列表
    vol1 = data["macd"]
    macd = vol1.tolist()
    # 获得dea列表
    vol2 = data["dea"]
    dea = vol2.tolist()
    # 获得diff列表
    vol3 = data["diff"]
    diff = vol3.tolist()
    return(macd,dea,diff)


def show_stockDetails(request):
    stockDetails=stock_details
    ts_code = request.session.get('global_ts_code')
    # 创建本地变量
    categoryData0, values0, volume0, macd0, dea0, diff0 = deal_Daily(ts_code)
    categoryData1, values1, volume1, macd1, dea1, diff1 = deal_Weekly(ts_code)
    categoryData2, values2, volume2, macd2, dea2, diff2 = deal_Monthly(ts_code)
    daily_basic_data = del_daily_basic(ts_code)
    return render(request, 'stockDetails.html', locals())


def main(request):
    return render(request, "main.html")


