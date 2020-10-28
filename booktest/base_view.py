import jinja2
import requests
from django.shortcuts import HttpResponse
from django.views import View
from booktest.models import TestGridFS


class BannerView(View):
    def get(self, request, *args, **kwargs):
        # 获取数据模型
        try:
            resp = requests.get('http://127.0.0.1:8000/cms/config/getmodel/5a791725dd573c3574ee333f')
            model = resp.json()['data']
        except Exception as e:
            return HttpResponse('获取数据模型出错')
        tpl_file = open('booktest/index_banner.tpl')
        _template = jinja2.Template(tpl_file.read())
        html = _template.render(**model)
        tpl_file.close()
        return HttpResponse(html)


class CourseDetailView(View):
    def get(self, request, *args, **kwargs):
        # 获取数据模型
        try:
            resp = requests.get('http://127.0.0.1:8000/course/courseview/1')
            model = resp.json()['data']
        except Exception as e:
            return HttpResponse('获取数据模型出错')
        tpl_file = open('booktest/course_detail.tpl')
        _template = jinja2.Template(tpl_file.read())
        html = _template.render(**model)
        tpl_file.close()
        return HttpResponse(html)


# 测试GridFS文件读取和存储
class TestGridFSView(View):

    def post(self, request, *args, **kwargs):
        # 创建TestGridFS实例
        template = TestGridFS()
        # 读取文件并保存到template中
        with open('booktest/index_banner.tpl', 'rb+') as file:
            template.template.put(file, content_type='text/html')
            template.save()
        return HttpResponse(str(template.id))

    def get(self, request, *args, **kwargs):
        # 读取TestGridFS实例
        template = TestGridFS.objects.first()
        if template is None:
            return HttpResponse('未找到记录', content_type='text/plain')
        tpl = template.template.read()
        return HttpResponse(tpl, content_type='text/plain')
