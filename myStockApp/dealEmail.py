import smtplib
from email.mime.text import MIMEText
from email.header import Header

from django.http import JsonResponse
from django.shortcuts import render

from myStockApp.models import User


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
