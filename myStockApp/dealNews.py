import json
import time
import datetime
from django.core import serializers
import pandas as pd
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
import tushare as ts

from myStockApp.models import News

token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


# 自定义异常
class FError(Exception):
    pass


def show_news(request):
    dateValues = get_calendar()
    todayDate = str(dateValues[-1])
    try:
        endDate = time.strftime('%Y%m%d', time.localtime(time.time() + 86400))
        startDate = time.strftime('%Y%m%d', time.localtime(time.time() - 86400))  # 只要跨度一天的新闻>80条
        df = pro.news(src='sina', start_date=startDate, end_date=endDate)
        data = df.to_json(orient='index')  # dataframe转json
        temp_data = json.loads(data)
        new_list = []
        for i in temp_data:
            # dict转obj
            class DicToObj:
                def __init__(self, **entries):
                    self.__dict__.update(entries)

            r = DicToObj(**temp_data[i])
            new_list.append(r)
        return render(request, 'news.html',
                      {'news': new_list, 'dateList': dateValues, 'todayDate': json.dumps(todayDate)})
    except:
        src = "sina"
        newsDate = list(reversed(dateValues))
        for day in newsDate:
            try:
                print("数据库读入中")
                new_list = News.objects.filter(Q(src=src) & Q(datetime__contains=day)).values('id', 'src', 'datetime',
                                                                                              'title', 'channels',
                                                                                              'content')
                if len(new_list) == 0:
                    raise FError("数据库错误")  # 直接抛出异常，中断尝试，进行后一步操作
                else:
                    print("数据条数：", len(new_list))
                    print(src + "/" + day + "/数据库读取成功")
                    return render(request, 'news.html',
                                  {'news': new_list, 'dateList': dateValues, 'todayDate': json.dumps(todayDate)})

            except:
                print("暂无", day, "当天记录，继续尝试读取最近的记录")


def main_show_sina_news(request):
    dateValues = get_calendar()
    try:
        endDate = time.strftime('%Y%m%d', time.localtime(time.time() + 86400))
        startDate = time.strftime('%Y%m%d', time.localtime(time.time()))  # 只要跨度一天的新闻>80条
        df = pro.news(src='sina', start_date=startDate, end_date=endDate)
        json_newsList = df.to_json(orient='records', force_ascii=False)  # dataframe转json
        newsList = json.loads(json_newsList)
        newsList = json.dumps(newsList[:8])
        return HttpResponse(newsList)
    except:
        src = "sina"
        newsDate = list(reversed(dateValues))
        for day in newsDate:
            try:
                print("数据库读入中")
                new_list = News.objects.filter(Q(src=src) & Q(datetime__contains=day)).values('id', 'src', 'datetime',
                                                                                              'title', 'channels',
                                                                                              'content')
                if len(new_list) == 0:
                    raise FError("数据库错误")  # 直接抛出异常，中断尝试，进行后一步 操作
                else:
                    print("数据条数：", len(new_list))
                    print(src + "/" + day + "/数据库读取成功")
                    new_list = json.dumps(list(new_list)[:8])
                    return HttpResponse(new_list)
            except:
                print("暂无", day, "当天记录，继续尝试读取最近的记录")


def get_news(request):
    if request.is_ajax():
        response = {"err_msg": ""}
        src = request.POST.get('src_id')
        date = request.POST.get('news_date')  # ajax传过来获得的数据格式是2019-2-9
        day, startDate, endDate = formatDay(date)  # 获得的 2109-02-08（数据库使用） 和 21090208（tushare接口使用）
        try:
            print("数据库读入中")
            obj = News.objects.filter(Q(src=src) & Q(datetime__contains=day)).values('id', 'src', 'datetime', 'title',
                                                                                     'channels', 'content')
            if len(obj) == 0:
                raise FError("数据库错误")  # 直接抛出异常，中断尝试，进行后一步操作
            else:
                print("数据条数：", len(obj))
                print(src + "/" + date + "/数据库读取成功")
                data = json.dumps(list(obj))
                return HttpResponse(data)
        except:
            print("数据库不存在数据")
            try:
                df = pro.news(src=src, start_date=startDate, end_date=endDate)
                data = df.to_json(orient='records', force_ascii=False)  # dataframe转json,保留中文
                print(src + "/" + date + "/尝试Tushare接口读取成功")
                update_news(src, date)
                return HttpResponse(data)
            except:
                print("尝试Tushare接口读取失败，请检查网络连接")
                response['status'] = "error"
                response['err_msg'] = "数据库未更新,尝试Tushare接口读取失败，请检查网络连接"
                return JsonResponse(response)


# 只要本月数据，所以只获得本月已经过了的日期
def get_calendar():
    t_list = []
    nowDate = time.strftime('%m', time.localtime(time.time()))
    nowMonth = int(nowDate)
    for i in range(30):
        ctime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * i))
        t = ctime.split('-')
        if int(t[1]) < nowMonth:
            break
        else:
            t_list.append(ctime)
    values = list(reversed(t_list))
    # 返回的数据格式使2019-01-01
    return values


def formatDay(date):  # 格式话日期，将2019-2-9类型日期格式化为21090208类型和2109-02-08类型
    t = date.split('-')
    s = date.split('-')
    if int(t[1]) < 10:
        t[1] = '0' + str(int(t[1]))
        s[1] = '-0' + str(int(s[1]))
    if int(t[2]) < 10:
        t[2] = '0' + str(int(t[2]))
        s[2] = '-0' + str(int(s[2]))
        nextDay = '0' + str(int(t[2]) + 1)
    else:
        s[2] = '-' + str(int(s[2]))
        nextDay = str(int(t[2]) + 1)
    day = s[0] + s[1] + s[2]
    startDate = t[0] + t[1] + t[2]
    endDate = t[0] + t[1] + nextDay
    return day, startDate, endDate


def update_news(src, date):
    nowDate = int(time.strftime('%d', time.localtime(time.time())))  # 当前时间：日
    today = int(date.split('-')[2])  # 传过来的2019-2-9格式数据转化为 9 ，即时间：日
    startDate, endDate = formatDay(date)[1:3]
    # 如果要求的数据是是当天的或者是非常老旧的数据（已过30天的），则不给予更新数据库,不是，则更新没有数据，同时删除数据库老旧的数据
    if nowDate == today:
        print("数据不完整，暂不更新")
    if today < nowDate:
        if today + 30 < nowDate:
            print("数据老旧，不更新")
        else:
            df = pro.news(src=src, start_date=startDate, end_date=endDate)
            df['src'] = src
            data = df.to_json(orient='records', force_ascii=False)  # dataframe转json,保留中文
            dataDict_list = json.loads(data)  # 转换成化dict的list
            print("更新数据库中——")
            i = 0
            for dataDict in dataDict_list:
                try:
                    News.objects.create(**dataDict)
                    i = i + 1
                except:
                    print("此条更新失败")
            print("更新条数：", i)
            print("更新完成")
