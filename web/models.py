from django.db import models


# Create your models here.
class UserInfo(models.Model):
    # ORM在为我们创建数据库的时候可以为该字段创建索引 查询的时候比较快
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
    phone = models.CharField(verbose_name="手机号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
