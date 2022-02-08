"""
用户账户功能 注册 短信 登陆 注销
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse

from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSmsForm


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, "web/register.html", {"form": form})
    print(request.POST)
    form = RegisterModelForm(data=request.POST)
    # 拿到校验信息
    if form.is_valid():
        # 验证通过 写入数据库
        # 这条语句会自动剔除数据库中不需要的部分
        form.save()
        # data = form.cleaned_data
        # data.pop('code')
        # data.pop('confirm_password')
        # instance = models.UserInfo.objects.create(**data)
        return JsonResponse({"status": True, 'data': '/login/sms/'})
    return JsonResponse({"status": False, "error": form.errors})


def send_sms(request):
    """所有的验证不写在视图函数了，都放在钩子函数里面来"""
    print(request.POST)
    phone = request.POST.get('phone')
    print(phone)
    # 通过data把POST过来的数据交给form校验
    form = SendSmsForm(request, data=request.POST)
    # 只是校验手机号不能为空，格式是否正确
    if form.is_valid():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSmsForm()
        return render(request, 'web/login_sms.html', {'form': form})
    print(request.POST)
    form = LoginSmsForm(data=request.POST)
    if form.is_valid():
        # 用户信息放到session 保存登陆状态
        userObject = form.cleaned_data['phone']
        print(userObject)
        return JsonResponse({"status": True, "data": "/index/"})
    return JsonResponse({"status": False, "error": form.errors})
