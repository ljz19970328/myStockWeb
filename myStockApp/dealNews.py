import json
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
import tushare as ts
token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


def show_news(request):
    datevalues = get_calendar()
    endDate = time.strftime('%Y%m%d', time.localtime(time.time() + 86400))
    startDate = time.strftime('%Y%m%d', time.localtime(time.time() - 86400))  # 只要跨度一天的新闻>80条
    df = pro.news(src='eastmoney', start_date=startDate, end_date=endDate)
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
    return render(request, 'news.html', {'news': new_list, 'dateList': datevalues})


def get_news(request):
    if request.is_ajax():
        src = request.POST.get('src_id')
        date = request.POST.get('news_date')
        t = date.split('-')
        if int(t[1]) < 10:
            t[1] = '0'+str(int(t[1]))
        if int(t[2]) < 9:
            t[2] = '0' + str(int(t[2]))
            nextDay = '0' + str(int(t[2])+1)
        else:
            nextDay = str(int(t[2]) + 1)
        startDate = t[0]+t[1]+t[2]
        endDate =t[0]+t[1]+nextDay
        df = pro.news(src=src, start_date=startDate, end_date=endDate)
        data = df.to_json(orient='records',force_ascii=False)  # dataframe转json,保留中文
        return HttpResponse(data)


# 只要本月数据，所以只获得本月已经过了的日期
def get_calendar():
    t_list = []
    nowDate = time.strftime('%m', time.localtime(time.time()))
    nowMonth = int(nowDate)
    for i in range(30):
        ctime = time.strftime('%Y-%m-%d', time.localtime(time.time()-86400*i))
        t = ctime.split('-')
        if int(t[1]) < nowMonth:
            break
        else:
            t_list.append(ctime)
    values = list(reversed(t_list))
    return values

