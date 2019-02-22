import json
import time
from django.shortcuts import render, redirect, render_to_response
import tushare as ts
token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()


def show_news(request):
    endDate = time.strftime('%Y%m%d', time.localtime(time.time()+86400))
    startDate = time.strftime('%Y%m%d', time.localtime(time.time()-86400*2)) # 只要跨度三天的新闻

    df = pro.news(src='sina', start_date=startDate, end_date=endDate)
    data = df.to_json(orient='index')  # dataframe转json
    temp_data = json.loads(data)
    list=[]
    for i in temp_data:
        # dict转obj
        class DicToObj:
            def __init__(self, **entries):
                self.__dict__.update(entries)
        r = DicToObj(**temp_data[i])
        list.append(r)
    return render(request, 'news.html',{'news':list})