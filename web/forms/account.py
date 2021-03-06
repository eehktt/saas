# 创建基本的modelform
import requests
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_redis import get_redis_connection
import random
from web.forms.boostrap import BoostrapForm
from utils.encrypt import md5
from web import models
from utils.sms.sms import send_sms_single


class RegisterModelForm(BoostrapForm, forms.ModelForm):
    # 正则表达式匹配phone字段，不通过->报错
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3456789]\d{9}$', '手机号格式错误'), ])
    # 替换自动生成的密码
    password = forms.CharField(label='密码', widget=forms.PasswordInput(),
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': '密码长度需要大于8位',
                                   'max_length': '密码长度 不能大于64位',
                               })
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput(
                                           attrs={'placeholder': '请确认密码'}
                                       ),
                                       min_length=8,
                                       max_length=64,
                                       error_messages={
                                           'min_length': '密码长度需要大于8位',
                                           'max_length': '密码长度 不能大于64位',
                                       })
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        # 对UserInfo的字段排序
        fields = ["username", "password", "confirm_password", "email", "phone", "code"]

    def clean_username(self):
        # 局部钩子：先拿到值再返回回去
        username = self.cleaned_data.get("username")
        exist = models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError("用户名已存在")
        return username

    def clean_email(self):
        # 局部钩子：先拿到值再返回回去
        email = self.cleaned_data.get("email")
        exist = models.UserInfo.objects.filter(email=email).exists()
        if exist:
            raise ValidationError("邮箱已注册")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = md5(password)
        return password

    def clean_confirm_password(self):
        # self.cleaned_data : 已验证的所有字段的数据，不能用该方法取未验证的值, Django 是按照顺序做校验
        # 这时候cleaned_data里存储的password已经是秘文的了
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if password != confirm_password:
            raise ValidationError('两次输入的密码不一致')
        return confirm_password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        exist = models.UserInfo.objects.filter(phone=phone).exists()
        if exist:
            raise ValidationError('手机号已注册')
        return phone

    def clean_code(self):
        phone = self.cleaned_data.get('phone')
        code = self.cleaned_data.get('code')
        conn = get_redis_connection()
        #  -如果手机号校验未通过，抛出异常
        if not phone:
            raise ValidationError('非法请求')
        redis_code = conn.get(phone)
        if not redis_code:
            raise ValidationError('验证码失效，请重新获取')
        # redis 拿出来的数据是字节形式 需要解码为utf8 再做比较
        redis_str_code = redis_code.decode('utf-8')
        # 比较的时候格式化 去掉两端空白
        if redis_str_code != code.strip():
            raise ValidationError('验证码错误，请重新输入')
        return code


# 只用Form 所有的字段就得自己写了 不能用meta了
class LoginSmsForm(BoostrapForm, forms.Form):
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3456789]\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(label='验证码')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # 取用户对象 把用户对象给返回了 不需要再通过手机号取用户对象
        user_object = models.UserInfo.objects.filter(phone=phone).first()
        if not user_object:
            raise ValidationError('手机号未注册')
        return user_object

    def clean_code(self):
        user_object = self.cleaned_data.get('phone')
        code = self.cleaned_data.get('code')
        conn = get_redis_connection()
        #  -如果手机号校验未通过，抛出异常,不需再校验验证马子
        if not user_object:
            return code
        # 取到的是用户对象 继续获取里面的phone属性
        redis_code = conn.get(user_object.phone)  # 从redis中获取输入手机号的验证码
        if not redis_code:
            raise ValidationError('验证码失效，请重新获取')
        # redis 拿出来的数据是字节形式 需要解码为utf8 再做比较
        redis_str_code = redis_code.decode('utf-8')
        # 比较的时候格式化 去掉两端空白
        if redis_str_code != code.strip():
            raise ValidationError('验证码错误，请重新输入')
        return code


class LoginForm(BoostrapForm, forms.Form):
    username = forms.CharField(label='账号')
    # 加上render_value=True->代表不自动删除密码
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True),
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': '密码长度需要大于8位',
                                   'max_length': '密码长度 不能大于64位',
                               })
    code = forms.CharField(label='验证码')

    # 钩子将用户输入的密码转为md5再返回给视图
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = md5(password)
        return password

    def clean_code(self):
        code = self.cleaned_data['code']
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码失效，请重新获取')
        # 先去空格再转成大写
        elif session_code.strip().upper() != code.upper():
            raise ValidationError('验证码错误，请重新输入')
        return code

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


# 和和数据库没关系，不用modelform，只对数据进行校验
class SendSmsForm(forms.Form):
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3456789]\d{9}$', '手机号格式错误'), ])

    def clean_phone(self):
        """手机号校验的钩子"""
        phone = self.cleaned_data.get('phone')
        tpl = self.request.POST.get('tpl')
        # 校验数据库中是否已有手机号
        exist = models.UserInfo.objects.filter(phone=phone).exists()
        code = random.randrange(1000, 9999)
        # 判断短信模版
        if not tpl:
            raise ValidationError('模版错误')
        if tpl == 'login':
            if not exist:
                raise ValidationError('手机号未注册')
            sms = "您的登录验证码是:" + str(code) + "，有效期十分钟，如非本人操作请忽略。"
        elif tpl == 'register':
            if exist:
                raise ValidationError('手机号已注册')
            sms = "您的注册验证码是:" + str(code) + "，有效期十分钟，如非本人操作请忽略。"
        else:
            raise ValidationError('非法请求')
        # 为了操作校验 展示信息比较方便 将发短信 写入redis功能也写入此处
        # 发短信
        res = send_sms_single(phone, sms)
        if res['result'] != 'Success':
            print(res['result'])
            raise ValidationError("短信发送失败，{}".format(res['message']))
        # 验证马子写入redis 超时时间600s
        conn = get_redis_connection()
        conn.set(phone, code, ex=600)

        return phone

    # 重写init方法，获取视图函数传过来的request
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
