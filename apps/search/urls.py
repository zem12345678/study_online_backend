from django.conf.urls import url
from search.views import CourseSearchView, CourseSearchAllView, MediaSearchView

urlpatterns = [
    url(r'^search/course/list/(?P<page>\d+)/(?P<size>\d+)', CourseSearchView.as_view()),
    url(r'^search/course/getall/(?P<course_id>\d+)', CourseSearchAllView.as_view()),
    url(r'^search/getmedia/(?P<teachplan_id>\d+)', MediaSearchView.as_view()),
]
