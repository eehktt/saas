from django.conf.urls import url, include
from django.contrib import admin

from web.views import account

urlpatterns = [
    # 加上name属性方便反向解析
    url(r'^register/$', account.register, name='register'),
    url(r'^send/sms/$', account.send_sms, name='send_sms'),
]