import time


def getTradeDate(latest_time):
    """
    交易日为周一至周五，数据更新时间不同，所以要进行处理，保证此时的时间参数是可以获得tushare接口的数据
    :param latest_time:
    :return:
    """
    stamp = time.time()
    # 获取当前时间戳
    date = time.localtime(stamp)
    # 利用localtime()转换为时间数组
    hour = int(time.strftime('%H', date))
    day = (time.strftime('%a', date))
    trade_date = time.strftime('%Y%m%d', date)
    if day != 'Sat' or day != 'Sun' or day != 'Mon':  # 周2，3，4，5
        if hour > latest_time:
            # 时间戳为当天
            trade_date = time.strftime('%Y%m%d', date)  # 没有跟新的话时间戳减一天
        elif hour <= latest_time:
            # 时间戳为前一天
            trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400))  # 没有跟新的话时间戳减一天
    if day == 'Sat':  # 周6
        trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400))  # 周六无数据，则取周五，时间戳减一天
    if day == 'Sun':  # 周7
        trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400 * 2))  # 周日无数据，则取周五，时间戳减二天
    if day == 'Mon':  # 周1
        if hour > latest_time:
            # 时间戳为当天
            trade_date = time.strftime('%Y%m%d', date)  # 没有跟新的话时间戳减一天
        elif hour <= latest_time:
            # 时间戳为上周五
            trade_date = time.strftime('%Y%m%d', time.localtime(stamp - 86400 * 3))  # 周一没有跟新的话时间戳减三天
    # 返回的数据格式为20190225
    return trade_date
