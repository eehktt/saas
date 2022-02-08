from django.conf.urls import url, include

from app01.views import views

urlpatterns = [
    url(r'^sms/send/', views.sms_send),
    url(r'^sms/info/', views.sms_show_info),
    url(r'^register/', views.register, name='register'),  # 反向解析的时候需要加上namespace，即 app01:register
]
