from django.db import models


# Create your models here.
class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
        ('unknown', "未设置"),
    )

    name = models.CharField(max_length=32, unique=True, null=False)
    password = models.CharField(max_length=32, null=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    sex = models.CharField(max_length=32, choices=gender, default="未选择")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Stock(models.Model):
    ts_code = models.CharField(max_length=32, unique=True)  # Tushare接口搜索代码
    symbol = models.CharField(max_length=32, unique=True)  # 股票代码
    name = models.CharField(max_length=32, unique=True)  # 股票名称
    area = models.CharField(max_length=32)  # 股票地域
    industry = models.CharField(max_length=32)  # 股票行业
    market = models.CharField(max_length=32)  # 股票市场类型
    list_date = models.CharField(max_length=32)  # 股票上市时间

    def __str__(self):
        return self


class StockDetails(models.Model):
    ts_code = models.CharField(max_length=32, unique=True)
    exchange = models.CharField(max_length=32)
    chairman = models.CharField(max_length=32)
    manager = models.CharField(max_length=32)
    secretary = models.CharField(max_length=32)
    reg_capital = models.CharField(max_length=32)
    setup_date = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    introduction = models.TextField(null=True)
    website = models.CharField(max_length=32, null=True)
    email = models.EmailField(unique=True, null=True)
    employees = models.CharField(max_length=32, null=True)
    main_business = models.TextField(null=True)
    business_scope = models.TextField(null=True)

    def __str__(self):
        return self.ts_code


class UserStockDetails(models.Model):
    UserCollectionDetails_username = models.CharField(max_length=32, null=False)
    UserCollectionDetails_name = models.CharField(max_length=32, null=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.UserCollectionDetails_username


class News(models.Model):
    src = models.CharField(max_length=32)
    datetime = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    channels = models.CharField(max_length=32)
    content = models.TextField()


class DailyDate(models.Model):
    ts_code = models.CharField(max_length=32)
    trade_date = models.CharField(max_length=32)
    open = models.CharField(max_length=32)
    high = models.CharField(max_length=32)
    low = models.CharField(max_length=32)
    close = models.CharField(max_length=32)
    pre_close = models.CharField(max_length=32)
    change = models.CharField(max_length=32)
    pct_chg = models.CharField(max_length=32)
    vol = models.CharField(max_length=32)
    amount = models.CharField(max_length=32)


class WeeklyData(models.Model):
    ts_code = models.CharField(max_length=32)
    trade_date = models.CharField(max_length=32)
    open = models.CharField(max_length=32)
    high = models.CharField(max_length=32)
    low = models.CharField(max_length=32)
    close = models.CharField(max_length=32)
    pre_close = models.CharField(max_length=32, null=True)
    change = models.CharField(max_length=32, null=True)
    pct_chg = models.CharField(max_length=32, null=True)
    vol = models.CharField(max_length=32, null=True)
    amount = models.CharField(max_length=32, null=True)


class MonthlyDate(models.Model):
    ts_code = models.CharField(max_length=32)
    trade_date = models.CharField(max_length=32)
    open = models.CharField(max_length=32)
    high = models.CharField(max_length=32)
    low = models.CharField(max_length=32)
    close = models.CharField(max_length=32)
    pre_close = models.CharField(max_length=32, null=True)
    change = models.CharField(max_length=32, null=True)
    pct_chg = models.CharField(max_length=32, null=True)
    vol = models.CharField(max_length=32, null=True)
    amount = models.CharField(max_length=32, null=True)


class IndexData(models.Model):
    ts_code = models.CharField(max_length=32)
    trade_date = models.CharField(max_length=32)
    close = models.CharField(max_length=32)
    open = models.CharField(max_length=32)
    high = models.CharField(max_length=32)
    low = models.CharField(max_length=32)
    pre_close = models.CharField(max_length=32, null=True)
    change = models.CharField(max_length=32, null=True)
    pct_chg = models.CharField(max_length=32, null=True)
    vol = models.CharField(max_length=32, null=True)
    amount = models.CharField(max_length=32, null=True)
