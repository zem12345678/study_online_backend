from django.conf.urls import url
from learning.views import CourseMediaView

urlpatterns = [
    url(r'learning/course/getmedia/(?P<course_id>\w+)/(?P<teachplan_id>\w+)', CourseMediaView.as_view()),
]
