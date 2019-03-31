import datetime

import pandas as pd
from django.db.models import Q
from django.http import JsonResponse
from myStockApp.dealTradeDate import getTradeDate
import tushare as ts

from myStockApp.models import IndexData

token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


# 自定义异常
class FError(Exception):
    pass


def get_index(request):  # 获得当天大盘数据
    try:
        print("大盘指数数据：tushare读入中")
        trade_date = getTradeDate(16)  # 15时修盘，数据来源可能更新不及时，所以推后一时获取
        df_SZ = pro.index_daily(ts_code='399001.SZ', trade_date=trade_date)
        df_SZ['name'] = '深证成指'
        df_SH = pro.index_daily(ts_code='000001.SH', trade_date=trade_date)
        df_SH['name'] = '上证指数'
    except:
        print("大盘指数数据：tushare读入失败，请检查网络连接，数据库读入中")
        db_trade_date = IndexData.objects.all().values('trade_date').distinct()  # 找到数据库的日期集合
        db_recent_time = list(db_trade_date)[0]['trade_date']  # 取出最近的日期
        obj_SZ = IndexData.objects.filter(Q(ts_code='399001.SZ') & Q(trade_date=db_recent_time)).values("ts_code",
                                                                                                        "high",
                                                                                                        "change",
                                                                                                        "pct_chg")
        df_SZ = pd.DataFrame(list(obj_SZ))
        df_SZ['name'] = '深证成指'
        obj_SH = IndexData.objects.filter(Q(ts_code='399001.SZ') & Q(trade_date=db_recent_time)).values("ts_code",
                                                                                                        "high",
                                                                                                        "change",
                                                                                                        "pct_chg")
        df_SH = pd.DataFrame(list(obj_SH))
        df_SH['name'] = '上证指数'
    df = df_SZ.append(df_SH)
    json_indexList = df.to_json(orient='records', force_ascii=False)  # dataframe转json
    data = {
        "json_indexList": json_indexList,
    }
    return JsonResponse(data)


def get_index_line_chart(request):  # 获得大盘日线数据
    ts_code = request.POST.get('ts_code')
    try:
        print("大盘日线数据：tushare读入中")
        data = pro.index_daily(ts_code=ts_code)
        if len(data) == 0:
            raise FError("请检查网络")
    except:
        print("大盘日线数据：tushare读入失败，请检查网络连接，数据库读入中")
        obj = IndexData.objects.filter(ts_code=ts_code).values("trade_date", "high")
        data = pd.DataFrame(list(obj))
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
