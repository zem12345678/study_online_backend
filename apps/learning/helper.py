from utils import xrequests
from utils.xcommon import AttributeAccessor


class SearchClient:
    base_url = 'http://www.czstudy.com'

    def get_media(self, teachplan_id):
        # 请求search的获取媒资信息接口，并将结果封装返回调用方
        url = self.base_url + '/api/search/getmedia/' + teachplan_id
        response = xrequests.HTTPRequest(url).get()
        return AttributeAccessor(response)
