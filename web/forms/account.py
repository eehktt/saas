# 创建基本的modelform
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_redis import get_redis_connection
import random
from web import models
from utils.sms.sms import send_sms_single


class RegisterModelForm(forms.ModelForm):
    # 正则表达式匹配phone字段，不通过->报错
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3456789]\d{9}$', '手机号格式错误'), ])
    # 替换自动生成的密码
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(attrs={'placeholder': '请确认密码'}))
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        # 对UserInfo的字段排序
        fields = ["username", "password", "confirm_password", "email", "phone", "code"]

    def __init__(self):
        super().__init__()
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if name == 'confirm_password':
                pass
            else:
                # 格式化不能被用户控制 否则会信息泄漏甚至rce
                field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


# 和和数据库没关系，不用modelform，只对数据进行校验
class SendSmsForm(forms.Form):
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3456789]\d{9}$', '手机号格式错误'), ])

    def clean_phone(self):
        """手机号校验的钩子"""
        phone = self.cleaned_data.get('phone')
        # 校验数据库中是否已有手机号
        exist = models.UserInfo.objects.filter(phone=phone).exists()
        if exist:
            raise ValidationError('手机号已存在')

        # 为了操作校验 展示信息比较方便 将发短信 写入redis功能也写入此处
        # 发短信
        code = random.randrange(1000, 9999)
        res = send_sms_single(phone, "您的注册验证码是:" + str(code) + "，有效期十分钟，如非本人操作请忽略。")
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




