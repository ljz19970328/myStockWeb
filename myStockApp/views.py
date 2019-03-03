import os
from django.shortcuts import render, redirect
from myStockApp.models import User
from myStockApp.models import UserStockDetails
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.is_ajax():  # 判断是否ajax请求
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        response = {"user": None, "err_msg": ""}
        try:
            user = User.objects.get(name=username)
            if user.password == pwd:
                request.session["isLogin"] = username
                request.session.set_expiry(0)
                response['user'] = user.name
                return JsonResponse(response)
            else:
                response['err_msg'] = "用户名或者密码错误！"
        except:
            response['err_msg'] = "用户名不存在"
        return JsonResponse(response)
    else:
        # request.session['userName'] =request.POST.get("user")
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
        NULL = ''
        if verifyCode == vcode_session:
            if User.objects.filter(name=uname):
                response['err_msg'] = "用户名已存在"
            else:
                if password == rePassword and password != NULL:
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
    bgcolor = (random.randrange(100, 150), random.randrange(60, 120), 226)
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


def callMaster(request):
    userName = request.session.get('isLogin')
    NULL = ''
    if userName:
        if request.is_ajax():
            response = {"err_msg": ""}
            userInfo = User.objects.get(name=userName)
            if userInfo.email is not None:
                try:
                    email_info = request.POST.get('email_info')  # 输入框信息获取
                    title_info = request.POST.get('title_info')  # 输入框信息获取
                    sendMail(email_info, userInfo.email, title_info, userName)  # 把输入框信息导入邮件
                    response["err_msg"] = "success"
                except:
                    response['err_msg'] = "NULLfAIL"
            else:
                print('发送失败，邮箱可能为空')
                response["err_msg"] = "NULLfAIL"
            return JsonResponse(response)
        else:
            return render(request, "callMaster.html")
    else:
        return render(request, "login.html")



def sendMail(body, user_Email, tit, uSERname):
    smtp_server = 'smtp.qq.com'  # 服务器类型
    from_mail = '2774598919@qq.com'  # 服务器邮箱名
    mail_pass = 'sbeunviqnmsodefi'  # 服务器授权码
    receivers = ['1401651730@qq.com']  # 服务器站长邮箱，接收邮件，可设置为你的QQ邮箱或者其他邮箱
    userInfo = uSERname + " <" + user_Email + ">"
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header(userInfo, 'utf-8')
    message['To'] = Header("WebMaker", 'utf-8')
    subject = tit
    message['Subject'] = Header(subject, 'utf-8')
    try:
        s = smtplib.SMTP()
        s.connect(smtp_server, '25')
        s.login(from_mail, mail_pass)
        # s.sendmail(from_mail, to_mail+cc_mail, msg)
        s.sendmail(from_mail, receivers, message.as_string())
        s.quit()
    except smtplib.SMTPException as e:
        print("Error: %s" % e)


def personCenter(request):  # 个人中心——修改用户数据
    if request.is_ajax():
        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        response = {"userName": None, "err_msg": ""}
        NULL = ''
        if User.objects.filter(name=userName):
            if userName != NULL and passWord != NULL and sex != NULL and email != NULL:
                try:
                    User.objects.filter(name=userName).update(password=passWord, sex=sex, email=email)
                    response['userName'] = userName
                except:
                    response['err_msg'] = "修改失败"
            else:
                response['err_msg'] = "请检查输入"
        else:
            response['err_msg'] = "用户名不存在"
        return JsonResponse(response)
    else:
        return render(request, "personCenter.html")


def loginCheck(request):  # 用户登陆状态查询
    if request.is_ajax():
        response = {"isLogin": None, "err_msg": ""}
        userName = request.session.get("isLogin")
        if User.objects.filter(name=userName):
            response['isLogin'] = userName
        else:
            response['err_msg'] = "noLogin"
        return JsonResponse(response)
    else:
        return render(request, "personCenter.html")


def perAdd(request):  # 填充数据进入页面
    if request.is_ajax():
        response = {"userName": None, "err_msg": ""}
        userName = request.session.get("isLogin")
        NULL = ''
        if User.objects.filter(name=userName):
            userInfo = User.objects.get(name=userName)
            response['userName'] = userName
            response['password'] = userInfo.password
            response['sex'] = userInfo.sex
            response['email'] = userInfo.email
        else:
            response['err_msg'] = "noLogin"
        return JsonResponse(response)
    else:
        return render(request, "personCenter.html")


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


def logout(request):
    request.session["isLogin"] = ""
    return redirect('/index/')
