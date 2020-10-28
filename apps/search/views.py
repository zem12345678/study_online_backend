from rest_framework.views import APIView
from rest_framework.response import Response
from search.helper import ESClient, MediaESClient


class CourseSearchView(APIView):

    def get(self, request, page, size):
        page = int(page)
        size = int(size)
        grade = request.query_params.get('grade')
        query_string = request.query_params.get('keyword')
        mt = request.query_params.get('mt')
        st = request.query_params.get('st')
        course_id = request.query_params.get('course_id')
        r = ESClient('cz_course').search(query_string=query_string, grade=grade, mt=mt, st=st, course_id=course_id,
                                        page=page, size=size)
        return Response(r)


class CourseSearchAllView(APIView):

    def get(self, request, course_id):
        ret = {}
        r = ESClient('cz_course').search(course_id=course_id)
        if r['total'] > 0:
            for hit in r['hits']:
                ret[hit['id']] = hit
        return Response(ret)


class MediaSearchView(APIView):

    def get(self, request, teachplan_id):
        r = MediaESClient('cz_course_media').search(teachplan_id=teachplan_id)
        if r['total'] > 0:
            return Response(r['hits'][0])
        else:
            return Response()
