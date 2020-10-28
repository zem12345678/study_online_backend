from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from django.shortcuts import HttpResponse
from common.response_code import SERVER_ERROR


class MyAPIException(APIException):

    def __init__(self, detail=None, code=None):
        # 判断detail是否符合标准异常信息的格式-长度为3的元组
        if isinstance(detail, tuple) and len(detail) == 3:
            self._error_response = detail
        detail = self.default_detail
        if code is None:
            code = self.default_code
        super().__init__(detail=detail, code=code)

    def get_error_response(self):
        if hasattr(self, '_error_response'):
            return self._error_response
        else:
            return None


def standard_exception_handler(exc, context):
    # 封装自己的异常处理函数，用于抛出标准异常信息
    response = exception_handler(exc, context)
    if isinstance(exc, APIException):
        if isinstance(exc, MyAPIException):
            # 获取标准异常中的数据，组装返回数据
            success, code, message = exc.get_error_response()
            data = {'success': success, 'code': code, 'message': message, 'data': {}}
        else:
            data = {'success': SERVER_ERROR[0], 'code': SERVER_ERROR[1], 'message': exc.detail, 'data': {}}
        response.data = data
        response.status_code = 200

    return response


def cast_exception(code):
    # 封装异常抛出函数，统一处理
    raise MyAPIException(code)


# 封装页面错误信息
def handle_http_error(code):
    return HttpResponse('<h3>{}</h3>'.format(code[-1]))
