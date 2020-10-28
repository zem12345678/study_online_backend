import json
from utils import xrequests
from cms.serializers import CmsPageSerializer
from utils.xcommon import AttributeAccessor


class CmsClient:
    base_url = 'http://www.czstudy.com'

    def save_cms_page(self, cms_page):
        # 请求cms的添加页面接口，并将结果封装返回给调用方
        url = self.base_url + '/api/cms/page/save'
        serializer = CmsPageSerializer(data=cms_page)
        serializer.is_valid(raise_exception=True)
        response = xrequests.HTTPRequest(url).post(json.dumps(serializer.data))
        return AttributeAccessor(response)

    def post_page_quick(self, cms_page):
        url = self.base_url + '/api/cms/page/postPageQuick'
        serializer = CmsPageSerializer(data=cms_page)
        serializer.is_valid(raise_exception=True)
        response = xrequests.HTTPRequest(url).post(json.dumps(serializer.data))
        return AttributeAccessor(response)
