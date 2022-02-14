"""
用户账户功能 注册 短信 登陆 注销
"""
import datetime

from django.http import HttpResponse
from io import BytesIO
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from utils.image_check_code import check_code
from django.db.models import Q
from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSmsForm, LoginForm
from utils.uuid_util import get_order_id


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
        # 把存进去的用户拿出来 为他生成一条交易记录
        instance = form.save()
        policy_object = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        # 创建交易记录
        models.Transaction.objects.create(
            status=2,
            order=get_order_id(),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
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
        # 登陆模型返回的phone字段已经是用户对象 用户信息放到session 保存登陆状态
        userObject = form.cleaned_data['phone']
        request.session['user_id'] = userObject.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        return JsonResponse({"status": True, "data": "/index/"})
    return JsonResponse({"status": False, "error": form.errors})


def login(request):
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'web/login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # filter 只能构造简单的查询条件
        # 构造复杂查询条件用Q
        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        # ORM查询手机号或者邮箱是否和密码匹配
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(phone=username)).filter(password=password)
        if not user_object:
            form.add_error('username', '用户名或密码错误')
        # 登录成功 id写入session
        request.session['user_id'] = user_object.id
        # 设置两周过期时间
        request.session.set_expiry(60 * 60 * 24 * 14)
        return redirect('index')
    # 前端用fields.errors.0获取每个字段的错误信息
    return render(request, 'web/login.html', {'form': form})


def image_code(request):
    """生成图片验证码"""
    image_object, val = check_code()
    print(val)
    stream = BytesIO()

    image_object.save(stream, 'jpeg')
    # 用session不用redis是因为比较方便 刚好可生成唯一的标识
    # 用redis 生成随机字符串和写入用户浏览器cookie需要手动做 把随机字符串和code当成键值对写入redis
    # 发短信用redis是因为不需要生成随机标识 手机号就是随机标识
    request.session['image_code'] = val
    request.session.set_expiry(60)  # 过期时间 60s
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    # 可以通过别名直接找到路径
    return redirect('index')
