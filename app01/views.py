from django import forms
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render

from app01 import models
from utils.sms.sms import sms_info, sms_single_send
import random


# Create your views here.


def sms_send(request):
    """ 发送短信 """
    code = random.randrange(1000, 9999)
    # send_sms_single('15625715237','7066',code)
    # sms_single_send("15625715237", "您的验证码是：" + str(code))
    sms_single_send("15625715", "您有一条新的任务指派，请登陆系统查看")
    return HttpResponse('成功')


def sms_show_info(request):
    try:
        sms_info()
        return HttpResponse('成功')
    except Exception:
        return HttpResponse(status=500)


# 创建基本的modelform
class RegisterModelForm(forms.ModelForm):
    # 正则表达式匹配phone字段，不通过->报错
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3456789]\d{9}$', '手机号格式错误'), ])
    # 替换自动生成的密码
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ["username", "password", "confirm_password", "email", "phone", "code"]

    def __init__(self):
        super().__init__()
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # 格式化不能被用户控制 否则会信息泄漏甚至rce
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


def register(request):
    form = RegisterModelForm()
    return render(request, "register.html", {"form": form})
