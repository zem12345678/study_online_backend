from calendar import timegm
from datetime import datetime
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    """向jwt认证成功的返回数据添加用户相关信息"""
    payload = {
        'userid': user.id,
        'username': user.username,
        'userpic': user.userpic,
        'utype': 'admin' if user.is_superuser else 'teacher' if user.is_staff else 'student',
        'phone': user.phone,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload
