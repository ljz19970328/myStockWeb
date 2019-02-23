import json
import time
from django.shortcuts import render, redirect, render_to_response
import tushare as ts
token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


def show_news(request):
    date_list = get_calendar()
    endDate = time.strftime('%Y%m%d', time.localtime(time.time()+86400))
    startDate = time.strftime('%Y%m%d', time.localtime(time.time()-86400*2)) # 只要跨度三天的新闻
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
    return render(request, 'news.html', {'news': new_list, 'dateList': date_list})


def get_calendar():
    nowDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    t_list = []
    t = nowDate.split('-')
    nowMonth = int(t[1])
    for i in range(30):
        ctime = time.strftime('%Y-%m-%d', time.localtime(time.time()-86400*i))
        t = ctime.split('-')
        if int(t[1]) < nowMonth:
            break
        else:
            t_list.append(ctime)
    values = list(reversed(t_list))
    return values


