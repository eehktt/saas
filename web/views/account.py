"""
用户账户功能 注册 短信 登陆 注销
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
    form = RegisterModelForm()
    return render(request, "web/register.html", {"form": form})


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

