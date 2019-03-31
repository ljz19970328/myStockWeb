import heapq
import json
import datetime
import pandas as pd
import tushare as ts
from django.db.models import Q
from django.http import HttpResponse

from myStockApp.models import Stock, DailyDate

token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()
from myStockApp.dealTradeDate import getTradeDate


# 自定义异常
class FError(Exception):
    pass


# stock涨跌序列排序
def stock_fluctuation(request):
    how = request.POST.get('how')
    sort_name = request.POST.get('type')
    try:
        # 从tushare接口获得最新数据
        stockList = data_from_ts()
        if len(stockList) == 0:
            raise FError("数据库错误")  # 直接抛出异常，中断尝试，进行后一步操作
    except:
        # 从数据库获得数据库里离当前时间最新数据
        stockList = data_from_db()
    # 调用排序函数获得结果
    result = getMax_Min(how, sort_name, stockList)
    return HttpResponse(result)


def getMax_Min(how, sort_name, stockList):
    result = []
    if how == '1':
        high_1000 = heapq.nlargest(100, stockList, key=lambda s: s[sort_name])  # 选出前100大的元素
        high_1000 = json.dumps(high_1000, ensure_ascii=False)
        result = high_1000
    if how == '0':
        low_1000 = heapq.nsmallest(100, stockList, key=lambda s: s[sort_name])  # 选出前100小的元素
        low_1000 = json.dumps(low_1000, ensure_ascii=False)
        result = low_1000
    return result


def data_from_ts():
    stockList = []
    try:
        print("涨幅数据：tushare接口读入中")
        # 从tushare获得最新数据
        trade_date = getTradeDate(16)
        # 日线数据最晚更新时间16点
        df = pro.daily(trade_date=trade_date)
        stockData = df[['ts_code', 'pre_close', 'open', 'high', 'close', 'change', 'pct_chg', 'amount']]
        stock_name_list = Stock.objects.all().values_list('ts_code', 'name', 'symbol')
        # 数据库取出股票名称,股票代码 ,为queryset类型数据
        nameDFrame = pd.DataFrame(list(stock_name_list))
        # queryset类型数据转成DataFrame
        nameDFrame.columns = ['ts_code', 'name', 'symbol']
        # 重新添加列名
        resultDFrame = pd.merge(stockData, nameDFrame, on='ts_code')
        # 通过列名ts_code把两个frame拼接
        json_stockList = resultDFrame.to_json(orient='records', force_ascii=False)  # dataframe转json
        stockList = json.loads(json_stockList)  # json转list
    except:
        print("涨幅数据：检查网络情况，tushare数据获取失败")
    return stockList


def data_from_db():
    stockList = []
    try:
        print("涨幅数据：tushare读入失败，数据库读入中")
        db_trade_date = DailyDate.objects.all().values('trade_date').distinct()  # 找到数据库的日期集合
        db_recent_time = list(db_trade_date)[0]['trade_date']  # 取出最近的日期
        stock_name_list = Stock.objects.all().values_list('ts_code', 'name', 'symbol')
        obj_left = pd.DataFrame(list(stock_name_list))
        obj_left.columns = ['ts_code', 'name', 'symbol']
        try:
            obj_right = DailyDate.objects.filter(Q(trade_date=db_recent_time)).values('ts_code', 'pre_close', 'open',
                                                                                      'high', 'close', 'change',
                                                                                      'pct_chg',
                                                                                      'amount')
            if len(obj_right) == 0:
                raise FError("数据库错误")  # 直接抛出异常，中断尝试，进行后一步操作
            else:
                obj_right = pd.DataFrame(list(obj_right))
                result = pd.merge(obj_left, obj_right, on='ts_code')  # 两张数据表数据进行merge
                json_stockList = result.to_json(orient='records', force_ascii=False)  # dataframe转json
                stockList = json.loads(json_stockList)  # json转list
                return stockList
        except:
            print("涨幅数据：数据库不存在数据，请检查数据库")
    except:
        return stockList

    # trade_date = datetime.datetime.strptime(db_recent_time, "%Y%m%d")  # 日期字符串转化为date形式
    # pre_date = trade_date + datetime.timedelta(days=+1)  # 日期时间加1天
    # print(pre_date)
