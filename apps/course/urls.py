from django.conf.urls import url
from course.views import CourseBaseViewSet, CategoryViewSet, CourseMarketViewSet, TeachplanViewSet, CoursePicViewSet, \
    CourseSummaryView, CoursePreviewView, CoursePublishView, SaveMediaView


urlpatterns = [
    url(r'^course/coursebase/list/(?P<page>\d+)/(?P<size>\d+)', CourseBaseViewSet.as_view({'get': 'list'})),
    url(r'^course/coursebase/add', CourseBaseViewSet.as_view({'post': 'create'})),
    url(r'^course/coursebase/get/(?P<course_id>\d+)', CourseBaseViewSet.as_view({'get': 'retrieve'})),
    url(r'^course/coursebase/update/(?P<course_id>\d+)', CourseBaseViewSet.as_view({'put': 'update'})),
    url(r'^category/list$', CategoryViewSet.as_view({'get': 'list'})),
    url(r'^course/coursemarket/get/(?P<course_id>\d+)', CourseMarketViewSet.as_view({'get': 'retrieve'})),
    url(r'^course/coursemarket/update/(?P<course_id>\d+)', CourseMarketViewSet.as_view({'post': 'update'})),
    url(r'^course/teachplan/list/(?P<course_id>\d+)', TeachplanViewSet.as_view({'get': 'list'})),
    url(r'^course/teachplan/add$', TeachplanViewSet.as_view({'post': 'create'})),
    url(r'^course/coursepic/add$', CoursePicViewSet.as_view({'post': 'create'})),
    url(r'^course/coursepic/list/(?P<course_id>\d+)', CoursePicViewSet.as_view({'get': 'retrieve'})),
    url(r'^course/coursepic/delete/(?P<course_id>\d+)', CoursePicViewSet.as_view({'delete': 'destroy'})),
    url(r'^course/courseview/(?P<course_id>\d+)', CourseSummaryView.as_view()),
    url(r'^course/preview/(?P<course_id>\d+)', CoursePreviewView.as_view()),
    url(r'^course/publish/(?P<course_id>\d+)', CoursePublishView.as_view()),
    url(r'^course/savemedia', SaveMediaView.as_view()),
]
