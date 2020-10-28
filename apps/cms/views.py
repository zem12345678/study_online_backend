from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from cms.models import CmsSite, CmsTemplate, CmsPage, CmsConfig, SysDictionary
from cms.serializers import CmsSiteSerializer, CmsTemplateSerializer, CmsPageSerializer, CmsConfigSerializer, \
    SysDictionarySerializer
from common import exceptions, response_code, paginations
from cms import helper
from celery_tasks.cms.tasks import post_page


class CmsSiteViewSet(ListModelMixin, GenericViewSet):
    queryset = CmsSite.objects
    serializer_class = CmsSiteSerializer


class CmsTemplateViewSet(ListModelMixin, GenericViewSet):
    queryset = CmsTemplate.objects
    serializer_class = CmsTemplateSerializer


class CmsPageViewSet(ModelViewSet):
    queryset = CmsPage.objects
    serializer_class = CmsPageSerializer
    pagination_class = paginations.PathPagePagination
    lookup_field = 'id'
    lookup_url_kwarg = 'page_id'

    # 根据查询参数过滤查询集
    def filter_queryset(self, queryset):
        filters = {}
        # 精确匹配条件检查
        if self.request.query_params.get('siteId'):
            filters.update({'siteId': self.request.query_params.get('siteId')})
        if self.request.query_params.get('templateId'):
            filters.update({'templateId': self.request.query_params.get('templateId')})
        if self.request.query_params.get('pageType'):
            filters.update({'pageType': self.request.query_params.get('pageType')})
        # 模糊匹配条件检查
        if self.request.query_params.get('pageAlias'):
            filters.update({'pageAlias__contains': self.request.query_params.get('pageAlias')})
        if self.request.query_params.get('pageName'):
            filters.update({'pageName__contains': self.request.query_params.get('pageName')})
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def create(self, request, *args, **kwargs):
        # 检查唯一索引-siteId,pageWebPath,pageName三者的组合是否已经存在，存在就报错，否则创建
        queryset = self.get_queryset()
        filter_set = queryset.filter(pageWebPath=request.data.get('pageWebPath'), siteId=request.data.get('siteId'),
                                     pageName=request.data.get('pageName'))
        if filter_set:
            exceptions.cast_exception(response_code.CMS_ADDPAGE_EXISTS)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        # 修改destroy状态码为接口要求的200
        response.status_code = 200
        return response


class CmsConfigViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = CmsConfig.objects
    serializer_class = CmsConfigSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'model': serializer.data['model']})


class CmsPagePublishViewSet(ModelViewSet):
    queryset = CmsPage.objects
    serializer_class = CmsPageSerializer

    def public(self, request, *args, **kwargs):
        page_id = kwargs['page_id']
        # 获取页面html
        status, page_html = helper.get_page_html(page_id)
        if status != 0:
            exceptions.cast_exception(page_html)
        # 保存页面html
        status, cms_page = helper.save_html(page_id, page_html)
        if status != 0:
            exceptions.cast_exception(cms_page)
        # 向mq发送消息
        post_page.delay(page_id=page_id)
        return Response()

    def save(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_set = queryset.filter(pageName=request.data.get('pageName'), siteId=request.data.get('siteId'),
                                     pageWebPath=request.data.get('pageWebPath')).first()
        if filter_set:
            self.kwargs['id'] = filter_set.id
            return super().update(request, *args, **kwargs)
        else:
            return super().create(request, *args, **kwargs)

    def post_quick(self, request, *args, **kwargs):
        # cms一键发布
        result = self.save(request, *args, **kwargs)
        if not result.data:
            exceptions.cast_exception(response_code.FAIL)
        kwargs['page_id'] = result.data['pageId']
        result = self.public(request, *args, **kwargs)
        cms_site = CmsSite.objects.filter(id=request.data['siteId']).first()
        page_url = cms_site.siteDomain + cms_site.siteWebPath + request.data['pageWebPath'] + request.data['pageName']
        return Response({'pageUrl': page_url})


class SysDictionaryViewSet(ModelViewSet):
    queryset = SysDictionary.objects.all()
    serializer_class = SysDictionarySerializer
    lookup_field = 'd_type'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'dvalue': response.data.get('d_value')})
