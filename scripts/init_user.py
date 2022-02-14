import base

from web import models

models.UserInfo.objects.create(username='admin', email='admin@ee.hk.cn', phone='15555555555', password='admin123456')
