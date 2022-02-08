# author z 20220209
import hashlib
from django.conf import settings


def md5(string):
    """md5加密"""
    # 将配置文件的SECRET_KEY拿来当盐
    hash_obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # 加密
    hash_obj.update(string.encode('utf-8'))
    return hash_obj.hexdigest()
