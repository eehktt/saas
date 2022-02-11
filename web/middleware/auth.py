from django.utils.deprecation import MiddlewareMixin
from web import models


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        """
        如果返回值了，用户看到 不再往后走了
        如果用户已经登录 在request中给他赋值
        :param request:
        :return:
        """
        # 如果用户已经登录 在request中赋值
        # 如果session中没有user_id就赋值为0 -> 查不着
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        # 这里是自定义的
        request.tracer = user_object
