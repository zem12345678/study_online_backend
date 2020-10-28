import requests
import json


class HTTPRequest:

    def __init__(self, url=None):
        self.url = url

    @staticmethod
    def jsonify_resp(resp):
        try:
            return resp.json()
        except Exception:
            return {}

    def get(self, params=None):
        try:
            resp = requests.get(self.url, params=params)
        except Exception:
            resp = {}
        return self.jsonify_resp(resp)

    def post(self, data=None):
        try:
            resp = requests.post(self.url, data=data, headers={'Content-Type': 'application/json'})
        except Exception:
            resp = {}
        return self.jsonify_resp(resp)

    def put(self, data=None):
        try:
            resp = requests.put(self.url, data=data)
        except Exception:
            resp = {}
        return self.jsonify_resp(resp)

    def delete(self):
        try:
            resp = requests.delete(self.url)
        except Exception:
            resp = {}
        return self.jsonify_resp(resp)
