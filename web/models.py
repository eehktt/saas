from django.db import models


# Create your models here.
class UserInfo(models.Model):
    # ORM在为我们创建数据库的时候可以为该字段创建索引 查询的时候比较快
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
    phone = models.CharField(verbose_name="手机号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)


class PricePolicy(models.Model):
    # 价格策略
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )
    category = models.SmallIntegerField(verbose_name='收费类型', default=1, choices=category_choices)  # 数据库中为smallint类型
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')
    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='成员数')
    project_size = models.PositiveIntegerField(verbose_name='项目空间')
    pre_file_size = models.PositiveIntegerField(verbose_name='单文件大小')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Transaction(models.Model):
    """交易记录"""
    status_choice = (
        (1, '未支付'),
        (2, '已支付'),
        (3, '已取消'),
    )
    status = models.SmallIntegerField(verbose_name='交易状态', choices=status_choice)
    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引 查询的时候速度最快 值不能重复
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy' )
    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限制')
    price = models.IntegerField(verbose_name='支付价格')
    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)  # 默认为空
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    color_choices = (
        (1, '#56b8eb'),
        (2, '#f28033'),
    )
    name = models.CharField(verbose_name='任务名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=color_choices, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField('项目已用空间', default=0)
    star = models.BooleanField('星标', default=False)
    # bucket = models.CharField(verbose_name='对象存储桶', max_length=128)
    # region = models.CharField(verbose_name='对象存储区域', max_length=32)
    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class ProjectParticipants(models.Model):
    user = models.ForeignKey(verbose_name='项目参与者', to='UserInfo')
    project = models.ForeignKey(verbose_name='项目', to='Project')
    star = models.BooleanField(verbose_name='星标', default=False)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)