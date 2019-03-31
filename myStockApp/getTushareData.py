import json
import time

import pandas as pd
import tushare as ts
from myStockApp import models
token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


def get_daily():
    ts_list = models.Stock.objects.all().values('ts_code')  # 只取user列
    print(ts_list)
    for stock in ts_list:
        time.sleep(60/200)
        df = pro.daily(ts_code=stock['ts_code'], start_date='20180601')
        data = df.to_json(orient='records')  # dataframe转json
        dic = json.loads(data)  # json转dict
    #dic = df.to_dict()
        print(dic)
        for i in dic:
            models.DailyDate.objects.create(**i)


def get_weekly():
    ts_list = models.Stock.objects.all().values('ts_code')  # 只取user列
    print(ts_list)
    for stock in ts_list:
        time.sleep(60/200)
        df = pro.weekly(ts_code=stock['ts_code'], start_date='20150101')
        data = df.to_json(orient='records')  # dataframe转json
        dic = json.loads(data)  # json转dict
    #dic = df.to_dict()
        print(dic)
        for i in dic:
            models.WeeklyData.objects.create(**i)


def get_monthly():
    ts_list = models.Stock.objects.all().values('ts_code')[527:]  # 只取user列
    print(ts_list)
    for stock in ts_list:
        time.sleep(60/200)
        df = pro.monthly(ts_code=stock['ts_code'], start_date='20050101',end_date='20190324')
        data = df.to_json(orient='records')  # dataframe转json
        dic = json.loads(data)  # json转dict
    #dic = df.to_dict()
        print(dic)
        for i in dic:
            models.MonthlyDate.objects.create(**i)


def get_indexData():
    ts_list = ['399001.SZ','000001.SH']
    for code in ts_list:
        print(code)
        time.sleep(60/200)
        df = pro.index_daily(ts_code=code)
        data = df.to_json(orient='records')  # dataframe转json
        dic = json.loads(data)  # json转dict
    #dic = df.to_dict()
        print(dic)
        for i in dic:
            models.IndexData.objects.create(**i)
