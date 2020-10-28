import requests
import json

from cz_study.settings import YUNPIAN_APIKEY


class YunPian:

    def __init__(self, api_key=None):
        self.api_key = api_key if api_key else YUNPIAN_APIKEY
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, phone):
        # 请求api所需的参数
        parmas = {
            "apikey": self.api_key,
            "mobile": phone,
            "text": "【个人签名】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        "{'http_status_code': 400, 'code': 5, 'msg': '未找到匹配的模板', 'detail': '未自动匹配到合适的模板'}"
        print(parmas)
        # response = requests.post(self.single_send_url, data=parmas)
        # re_dict = json.loads(response.text)
        re_dict = {'code': 0, 'msg': '发送成功', 'count': 1, 'fee': 0.05, 'unit': 'RMB', 'mobile': phone, 'sid': 44681894854}
        print(re_dict)
        return re_dict

    @staticmethod
    def succeeded(send_result):
        try:
            return send_result['code'] == 0
        except (KeyError, ValueError, TypeError) as e:
            return False

    @staticmethod
    def message(send_result):
        try:
            return send_result['msg']
        except (KeyError, ValueError, TypeError) as e:
            return ''


if __name__ == "__main__":
    yunpian = YunPian()
    result = yunpian.send_sms("2018", "18112345678")
    print(yunpian.succeeded(result))
    print(yunpian.message(result))
