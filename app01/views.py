from django.http import HttpResponse
from django.shortcuts import render
from utils.sms.sms import sms_info, sms_single_send
import random

# Create your views here.



def sms_send(request):
    """ 发送短信 """
    code = random.randrange(1000, 9999)
    #send_sms_single('15625715237','7066',code)
    # sms_single_send("15625715237", "您的验证码是：" + str(code))
    sms_single_send("15625715237", "您有一条新的任务指派，请登陆系统查看")
    return HttpResponse('成功')

def sms_show_info(request):
    try:
        sms_info()
        return HttpResponse('成功')
    except Exception:
        return HttpResponse(status=500)
