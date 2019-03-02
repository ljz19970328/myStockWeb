import time
import heapq
import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
import json
import pandas as pd
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


def get_trade_date(latest_time):
    """
    交易日为周一至周五，数据更新时间不同，所以要进行处理，保证此时的时间参数是可以获得tushare接口的数据
    :param latest_time:
    :return:
    """
    stamp = time.time()
    # 获取当前时间戳
    date = time.localtime(stamp)
    # 利用localtime()转换为时间数组
    hour = int(time.strftime('%H', date))
    day = (time.strftime('%a', date))
    if day != 'Sat' or day != 'Sun' or day != 'Mon':  # 周2，3，4，5
        if hour > latest_time:
            # 时间戳为当天
            trade_date = time.strftime('%Y%m%d', date)  # 没有跟新的话时间戳减一天
        elif hour <= latest_time:
            # 时间戳为前一天
            trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400))  # 没有跟新的话时间戳减一天
    if day == 'Sat':  # 周6
        trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400))  # 周六无数据，则取周五，时间戳减一天
    if day == 'Sun':  # 周7
        trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400 * 2))  # 周日无数据，则取周五，时间戳减二天
    if day == 'Mon':  # 周1
        if hour > latest_time:
            # 时间戳为当天
            trade_date = time.strftime('%Y%m%d', date)  # 没有跟新的话时间戳减一天
        elif hour <= latest_time:
            # 时间戳为上周五
            trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400 * 3))  # 周一没有跟新的话时间戳减三天
    # 返回的数据格式为20190225
    return trade_date


def query_stockDetails(request):
    ts_code = request.POST.get('ts_code')
    request.session['global_ts_code'] = ts_code
    global stock_details
    stock_details = StockDetails.objects.filter(ts_code=ts_code)
    response = {"msg": ""}
    return JsonResponse(response)


# 获得股票基本面数据 交易日每日15点～17点之间更新
def del_daily_basic(ts_code):
    trade_date = get_trade_date(17)
    # 基本面数据最晚更新时间17点
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


# stock涨跌序列排序
def stock_fluctuation(request):
    how = request.POST.get('how')
    sort_name = request.POST.get('type')

    trade_date = get_trade_date(16)
    # 日线最晚更新时间16点
    df = pro.daily(trade_date=trade_date)
    stockData = df[['ts_code', 'pre_close', 'open', 'high','close','change','pct_chg','amount']]
    try:
        stock_name_list = Stock.objects.all().values_list('ts_code','name','symbol')
        # 数据库取出股票名称,股票代码 ,为queryset类型数据
        nameFrame = pd.DataFrame(list(stock_name_list))
        # queryset类型数据转成DataFrame
        nameFrame.columns = ['ts_code', 'name', 'symbol']
        # 重新添加列明
        result = pd.merge(stockData, nameFrame,on='ts_code')
        # 通过列名ts_code把两个frame拼接
    except:
        print("数据库查询失败")
    json_stockList = result.to_json(orient='records', force_ascii=False)  # dataframe转json
    json_stockList = json.loads(json_stockList)  # json转list
    if(how == '1'):
        high_1000 = heapq.nlargest(100, json_stockList, key=lambda s: s[sort_name])  # 选出前100大的元素
        high_1000 = json.dumps(high_1000, ensure_ascii=False)
        stockList = high_1000
    if(how == '0'):
        low_1000 = heapq.nsmallest(100, json_stockList, key=lambda s: s[sort_name])  # 选出前100小的元素
        low_1000 = json.dumps(low_1000, ensure_ascii=False)
        stockList = low_1000
    return HttpResponse(stockList)


def get_index(request):
    trade_date = get_trade_date(16)  # 15时修盘，数据来源可能更新不及时，所以推后一时获取
    df_SZ = pro.index_daily(ts_code='399001.SZ', trade_date=trade_date)
    df_SZ['name'] = '深证成指'
    df_SH = pro.index_daily(ts_code='000001.SH', trade_date=trade_date)
    df_SH['name'] = '上证指数'
    df = df_SZ.append(df_SH)
    json_indexList = df.to_json(orient='records', force_ascii=False)  # dataframe转json
    data = {
        "json_indexList": json_indexList,
    }
    return JsonResponse(data)


def get_index_line_chart(request):
    ts_code = request.POST.get('ts_code')
    data = pro.index_daily(ts_code=ts_code)
    lineChart_time = data["trade_date"]
    lineChart_data = data["high"]
    timeList = lineChart_time.tolist()
    dataList = lineChart_data.tolist()
    categoryData = list(reversed(timeList))
    values = list(reversed(dataList))
    data = {
        "categoryData": categoryData,
        "values": values,
    }
    return JsonResponse(data)




def main(request):
    return render(request, "main.html")
