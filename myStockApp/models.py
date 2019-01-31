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
    email = models.EmailField(unique=True,null=True,blank=True)
    sex = models.CharField(max_length=32, choices=gender, default="未选择")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
