import re
from datetime import datetime, timedelta
from rest_framework import serializers
from ucenter.models import CzUser, VerifyCode
from cz_study import settings
from rest_framework.validators import UniqueValidator


class SmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    # 验证手机号码
    def validate_phone(self, phone):
        # 验证手机号码是否合法
        if not re.match(settings.REGEX_MOBILE, phone):
            raise serializers.ValidationError('手机号码非法')
        # 验证手机是否已经注册
        if CzUser.objects.filter(phone=phone).count():
            raise serializers.ValidationError('用户已经存在')
        # 验证码发送是否过于频繁
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(phone=phone, add_time__gt=one_minute_ago).count():
            raise serializers.ValidationError('距离上次发送未超过60s')
        return phone


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4)
    phone = serializers.CharField(required=True, allow_blank=False, validators=[
        UniqueValidator(queryset=CzUser.objects.all(), message='用户已经存在')
    ])
    password = serializers.CharField(write_only=True)

    def validate_code(self, code):
        verify_codes = VerifyCode.objects.filter(phone=self.initial_data['phone']).order_by('-add_time')
        if verify_codes:
            last_code = verify_codes[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_code.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_code.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs['username'] = attrs['phone']
        del attrs['code']
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CzUser
        fields = ('code', 'phone', 'password')
