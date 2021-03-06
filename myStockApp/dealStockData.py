import os
import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
import json
import pandas as pd
from myStockApp.dealTradeDate import getTradeDate
from myStockApp.models import  DailyDate, MonthlyDate, WeeklyData
from myStockApp.models import StockDetails
import tushare as ts


token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 自定义异常
class FError(Exception):
    pass


def query_stockDetails(request):
    ts_code = request.POST.get('ts_code')
    request.session['global_ts_code'] = ts_code
    global stock_details
    stock_details = StockDetails.objects.filter(ts_code=ts_code)
    response = {"msg": ""}
    return JsonResponse(response)


# 获得股票基本面数据 交易日每日15点～17点之间更新
def del_daily_basic(ts_code):
    # 从dealTradeDate引用getTradeDate
    trade_date = getTradeDate(17)
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
    try:
        df = pro.daily(ts_code=ts_code, start_date='20180601', end_date="20190322")
        trade_date = df["trade_date"]
        k_line_data = df[["open", "close", "low", "high"]]
        vol = df["vol"]
    except:
        obj = DailyDate.objects.filter(ts_code=ts_code).values("trade_date", "open", "close", "low", "high", "vol")
        df = pd.DataFrame(list(obj))
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
    macd, dea, diff = cal_macd(df)
    # 返回值
    return categoryData, values, volume, macd, dea, diff


# 获得周线数据，提取周k线所需数据
def deal_Weekly(ts_code):
    try:
        df = pro.weekly(ts_code=ts_code, start_date='20160101')
        trade_date = df["trade_date"]
        k_line_data = df[["open", "close", "low", "high"]]
        vol = df["vol"]
    except:
        obj = WeeklyData.objects.filter(ts_code=ts_code).values("trade_date", "open", "close", "low", "high", "vol")
        df = pd.DataFrame(list(obj))
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
    macd, dea, diff = cal_macd(df)
    # 返回值
    return categoryData, values, volume, macd, dea, diff


# 获得月线数据，提取月k线所需数据
def deal_Monthly(ts_code):
    try:
        df = pro.monthly(ts_code=ts_code, start_date='19910101')
        trade_date = df["trade_date"]
        k_line_data = df[["open", "close", "low", "high"]]
        vol = df["vol"]
    except:
        obj = MonthlyDate.objects.filter(ts_code=ts_code).values("trade_date", "open", "close", "low", "high", "vol")
        df = pd.DataFrame(list(obj))
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
    macd, dea, diff = cal_macd(df)
    # 返回值
    return categoryData, values, volume, macd, dea, diff


def cal_macd(data):
    # data是包含高开低收成交量的标准dataframe
    # short_,long_,m分别是macd的三个参数
    # 返回值是diff,dea,macd三个list
    short_ = 12
    long_ = 26
    m = 9
    data = data.reindex(index=data.index[::-1])
    data['diff'] = data['close'].ewm(adjust=False, alpha=2 / (short_ + 1), ignore_na=True).mean() - \
                   data['close'].ewm(adjust=False, alpha=2 / (long_ + 1), ignore_na=True).mean()
    data['dea'] = data['diff'].ewm(adjust=False, alpha=2 / (m + 1), ignore_na=True).mean()
    data['macd'] = 2 * (data['diff'] - data['dea'])
    # 获得macd列表
    vol1 = data["macd"]
    macd = vol1.tolist()
    # 获得dea列表
    vol2 = data["dea"]
    dea = vol2.tolist()
    # 获得diff列表
    vol3 = data["diff"]
    diff = vol3.tolist()
    return macd, dea, diff


def show_stockDetails(request):
    stockDetails = stock_details
    ts_code = request.session.get('global_ts_code')
    # 创建本地变量
    categoryData0, values0, volume0, macd0, dea0, diff0 = deal_Daily(ts_code)
    categoryData1, values1, volume1, macd1, dea1, diff1 = deal_Weekly(ts_code)
    categoryData2, values2, volume2, macd2, dea2, diff2 = deal_Monthly(ts_code)
    daily_basic_data = del_daily_basic(ts_code)
    return render(request, 'stockDetails.html', locals())


def companyLogo_image(request):
    code = request.session.get('global_ts_code')[0:6]
    image_path = BASE_DIR + '\myStockApp\static\\companyLogo\\' + code + '.png'
    image_data = open(image_path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def main(request):
    return render(request, "main.html")
