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


def show_stockDetails(request):
    return render(request, 'stockDetails.html', {'stockDetails': stock_details})


def deal_Daily(request):
    ts_code = request.session.get('global_ts_code')
    response = {"msg": ""}
    try:
        df = pro.daily(ts_code=ts_code, start_date='20180101', end_date='20181101')
        trade_date = df["trade_date"]
        k_line_data = df[["open", "close", "low", "high"]]
        trade_date = trade_date.tolist()
        var1 = np.array(k_line_data)
        k_line_data = var1.tolist()
        return render(request, 'stockDataView.html', {'categoryData': trade_date, 'values': k_line_data})
    except:
        print("请求繁忙，请稍后再试")
        response["msg"] = "请求繁忙，请稍后再试"
    return JsonResponse(response)


def deal_Weekly(stock_NO):
    df = pro.weekly(ts_code=stock_NO, start_date='20180101', end_date='20181101')


def deal_Monthly(stock_NO):
    df = pro.monthly(ts_code=stock_NO, start_date='20180101', end_date='20181101')

def main(request):
    return render(request,"main.html")


