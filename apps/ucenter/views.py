from random import choice
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from ucenter.models import VerifyCode
from ucenter.serializers import SmsSerializer, UserRegisterSerializer
from utils.xsms import YunPian


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = SmsSerializer
    authentication_classes = []

    # 生成四位数字的验证码
    def generate_code(self):
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证是否合法
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        yun_pian = YunPian()
        # 生成验证码
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code, phone)
        if not yun_pian.succeeded:
            return Response({'phone': yun_pian.message(sms_status)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            record = VerifyCode(code=code, phone=phone)
            record.save()
            return Response({'phone': phone}, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, GenericViewSet):
    """
    创建用户
    """
    serializer_class = UserRegisterSerializer
    authentication_classes = []
