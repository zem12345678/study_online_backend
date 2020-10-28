from django.conf.urls import url, include
from rest_framework_mongoengine.routers import SimpleRouter
from booktest.views import BookInfoViewSet, HeroInfoViewSet
from booktest.base_view import BannerView, TestGridFSView, CourseDetailView


# 实例化router
router = SimpleRouter()
# 注册视图集
router.register('book', BookInfoViewSet)
router.register('hero', HeroInfoViewSet)


urlpatterns = [
    url(r'test/', include(router.urls)),
    url(r'test/banner', BannerView.as_view()),
    url(r'test/course', CourseDetailView.as_view()),
    url(r'test/gridfs', TestGridFSView.as_view()),
]

