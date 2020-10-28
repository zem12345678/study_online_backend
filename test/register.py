import requests
base_url = 'http://localhost:8000'


def test_sms_code():
    url = base_url + '/auth/code'
    resp = requests.post(url, json={'phone': '18112345678'})
    print(resp.json())


def test_register(code):
    url = base_url + '/auth/register'
    resp = requests.post(url, json={'phone': '18112345678', 'code': code, 'password': '123456'})
    print(resp.json())


if __name__ == '__main__':
    # test_sms_code()
    test_register('8827')
