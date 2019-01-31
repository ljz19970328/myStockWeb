import os
from django.shortcuts import render, redirect
from myStockApp.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request, 'index.html')


def login(request):
    # if request.method == "POST":
    if request.is_ajax():  # 判断是否ajax请求
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        response = {"user": None, "err_msg": ""}
        try:
            user = User.objects.get(name=username)
            if user.password == pwd:
                response['user'] = user.name
                return JsonResponse(response)
            else:
                response['err_msg'] = "用户名或者密码错误！"
        except:
            response['err_msg'] = "用户名不存在"
        return JsonResponse(response)
    else:
        return render(request, "login.html")


def register(request):
    if request.is_ajax():
        uname = request.POST.get('user')
        password = request.POST.get('pwd')
        rePassword = request.POST.get('rpwd')
        # 获取用户输入的验证码
        verifyCode = request.POST.get('vcode')
        # 获取session中的验证码
        vcode_session = request.session.get('verify_code')
        response = {"user": None, "err_msg": ""}
        NULL=''
        if verifyCode == vcode_session:
            if User.objects.filter(name=uname):
                response['err_msg'] = "用户名已存在"
            else:
                if password == rePassword and password!=NULL :
                    try:
                        User.objects.create(name=uname, password=password)
                        response['user'] = uname
                    except:
                        response['err_msg'] = "注册失败"
                else:
                    response['err_msg'] = "请检查输入"
        else:
            response['err_msg'] = "验证码错误"
        return JsonResponse(response)
    else:
        return render(request, "register.html")


def verify_code(request):
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 80
    height = 40
    # 2，创建画面对象python manage.py makemigrations
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    # 5，定义验证码的备选值
    str1 = 'mnbvcxzABCD123EFGHIJKqwertyuiop456LMNOPQRSasdfghjkl789TUVWXYZ0'
    # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象
    str = BASE_DIR + '\myStockApp\static\\font\FreeMono.ttf'
    font = ImageFont.truetype(str, 28)
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 9，绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((20, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((40, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((55, 2), rand_str[3], font=font, fill=fontcolor)
    # 9，用完画笔，释放画笔
    del draw
    # 10，存入session，用于做进一步验证
    request.session['verify_code'] = rand_str
    # 11，内存文件操作
    buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def logout(request):
    return redirect('/index/')
