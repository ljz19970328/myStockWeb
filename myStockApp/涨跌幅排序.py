import tushare as ts
import json


token = "e2fe953eb0ec041fe719d9c45c3fd632ea37635b415bd3839d747f19"
ts.set_token(token)
pro = ts.pro_api()
df = pro.daily(trade_date='20190215')
data=df[['ts_code','pre_close','open','close','pct_chg']]
data=data.to_json(orient='index')
temp_data = json.loads(data)
list=[]
res=[]
for i in temp_data:
        # dict转obj
    class DicToObj:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    r = DicToObj(**temp_data[i])
    list.append(r)
# for i in list:
#  print(i.pct_chg)

#--快排算法
def part(ll, begin, end):
    k = ll[end].pct_chg
    i = begin - 1
    for j in range(begin, end):
        if ll[j].pct_chg<= k:
            i += 1
            ll[j], ll[i] = ll[i], ll[j]
    ll[end], ll[i + 1] = ll[i + 1], ll[end]
    return i + 1


def qsort1(ll, l, r):
    if l < r:
        mid = part(ll, l, r)
        qsort1(ll, l, mid - 1)
        qsort1(ll, mid + 1, r)
qsort1(list, 0, len(list) - 1)
#！！！！快排算法
for i in list:
 print(i.pct_chg)