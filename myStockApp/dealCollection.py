import json

import tushare as ts
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from myStockApp.dealTradeDate import getTradeDate
from myStockApp.models import User, UserStockDetails, Stock

token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


def show_myCollection(request):  # 在主页面显示我的收藏
    LoginName = request.session.get("isLogin")
    response = {"msg": ""}
    trade_date = getTradeDate(16)
    if User.objects.filter(name=LoginName):
        try:
            userStock = UserStockDetails.objects.filter(Q(UserCollectionDetails_username=LoginName))  # 获取用户收藏股票代码
            Stock_C_list = []
            for stock in userStock:
                collection_stock = Stock.objects.get(ts_code=stock.UserCollectionDetails_name)  # 查询收藏股票的具体信息
                # 日线最晚更新时间16点
                df = pro.daily(ts_code=collection_stock.ts_code, trade_date=trade_date)
                if list(df['pct_chg'])[0] >= 0:  # 判断涨跌
                    color = "#dd2200"  # 红色
                else:
                    color = "#00FA9A"  # 绿色
                temp = {"ts_code": collection_stock.ts_code, "name": collection_stock.name, "industry": collection_stock.industry, "color": color}
                Stock_C_list.append(temp)
            json_C_list = json.dumps(Stock_C_list[0:11], ensure_ascii=False)
            response['msg'] = 'ok'
            return HttpResponse(json_C_list)
        except:
            response['msg'] = 'flase'
            print("查询失败")
            return JsonResponse(response)
    else:
        response['msg'] = 'noLogin'
        return JsonResponse(response)


def show_collection_stockDetails(request):  # 我的收藏页面数据填充
    LoginName = request.session.get("isLogin")
    response = {"msg": ""}
    if User.objects.filter(name=LoginName):
        try:
            stock_data = UserStockDetails.objects.filter(Q(UserCollectionDetails_username=LoginName))  # 获取用户收藏股票代码
            Stock_C_list = []
            for stock in stock_data:
                menu = Stock.objects.get(ts_code=stock.UserCollectionDetails_name)  # 查询收藏股票的具体信息
                Stock_C_list.append(menu)
            response['msg'] = 'ok'
            return render(request, 'myCollectionStock.html', {'searchResults': Stock_C_list})  # 渲染数据进入我的收藏界面
        except:
            response['msg'] = 'flase'
            print("查询失败")
        return JsonResponse(response)
    else:
        response['msg'] = 'noLog'
        return JsonResponse(response)
    # return render(request, 'login.html')


def collection_Stock(request):  # 增加股票收藏
    userName = request.session.get("isLogin")
    response = {"err_msg": ""}
    if User.objects.filter(name=userName):
        if request.is_ajax():
            collection_Name = request.POST.get('collection_info')
            # 判断该用户是否已经收藏过该股票
            if (UserStockDetails.objects.filter(UserCollectionDetails_name=collection_Name,
                                                UserCollectionDetails_username=userName)):
                response["err_msg"] = "false"
            else:
                response["err_msg"] = "true"
                UserStockDetails.objects.create(UserCollectionDetails_username=userName,
                                                UserCollectionDetails_name=collection_Name)
            return JsonResponse(response)
        else:
            return render(request, "stockDetails.html")
    else:
        response["err_msg"] = "noLogin"
        return JsonResponse(response)


def del_collection_Stock(request):  # 删除股票收藏
    if request.is_ajax():
        # NULL="";
        response = {"err_msg": ""}
        userName = request.session.get("isLogin")
        if User.objects.filter(name=userName):
            try:
                del_collection_Name = request.POST.get('del_collection_info')
                UserStockDetails.objects.filter(UserCollectionDetails_name=del_collection_Name,
                                                UserCollectionDetails_username=userName).delete()
                response['err_msg'] = "true"
            except:
                response['err_msg'] = "false"
        else:
            return render(request, "login.html")
        return JsonResponse(response)
    else:
        return render(request, "myCollectionStock.html")
