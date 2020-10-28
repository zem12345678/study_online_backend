from django.views import View
from django.shortcuts import HttpResponse
from cms.helper import get_page_html
from common.exceptions import handle_http_error


class CmsPagePreviewView(View):

    def get(self, request, page_id):
        status, page_html = get_page_html(page_id)
        if status != 0:
            return handle_http_error(page_html)
        return HttpResponse(page_html)


