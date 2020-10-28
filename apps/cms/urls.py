from django.conf.urls import url, include
from rest_framework_mongoengine.routers import SimpleRouter
from cms.views import CmsSiteViewSet, CmsTemplateViewSet, CmsPageViewSet, CmsConfigViewSet, CmsPagePublishViewSet, \
    SysDictionaryViewSet
from cms import admin_views
from cms.base_view import CmsPagePreviewView


router = SimpleRouter()
router.register('cms_template', admin_views.CmsTemplateViewSet)
router.register('cms_site', admin_views.CmsSiteViewSet)

urlpatterns = [
    url(r'admin/', include(router.urls)),
    url(r'^cms/site/list', CmsSiteViewSet.as_view({'get': 'list'})),
    url(r'^cms/template/list', CmsTemplateViewSet.as_view({'get': 'list'})),
    url(r'^cms/page/add', CmsPageViewSet.as_view({'post': 'create'})),
    url(r'^cms/page/list/(?P<page>\d+)/(?P<size>\d+)', CmsPageViewSet.as_view({'get': 'list'})),
    url(r'^cms/page/get/(?P<page_id>\w+)', CmsPageViewSet.as_view({'get': 'retrieve'})),
    url(r'^cms/page/edit/(?P<page_id>\w+)', CmsPageViewSet.as_view({'put': 'update'})),
    url(r'^cms/page/del/(?P<page_id>\w+)', CmsPageViewSet.as_view({'delete': 'destroy'})),
    url(r'^cms/config/getmodel/(?P<id>\w+)', CmsConfigViewSet.as_view({'get': 'retrieve'})),
    url(r'^cms/preview/(?P<page_id>\w+)', CmsPagePreviewView.as_view()),
    url(r'^cms/page/postPage/(?P<page_id>\w+)$', CmsPagePublishViewSet.as_view({'post': 'public'})),
    url(r'^sys/dictionary/get/(?P<d_type>\d+)$', SysDictionaryViewSet.as_view({'get': 'retrieve'})),
    url(r'^cms/page/save$', CmsPagePublishViewSet.as_view({'post': 'save'})),
    url(r'^cms/page/postPageQuick', CmsPagePublishViewSet.as_view({'post': 'post_quick'})),
]
