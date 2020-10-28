from rest_framework.views import APIView
from rest_framework.response import Response
from common.exceptions import cast_exception
from common import response_code
from learning.helper import SearchClient


class CourseMediaView(APIView):

    def get(self, request, course_id, teachplan_id):
        result = SearchClient().get_media(teachplan_id)
        if not result.success or not result.data.media_url:
            cast_exception(response_code.COURSE_MEDIS_URLISNULL)
        return Response({'fileUrl': result.data.media_url})
