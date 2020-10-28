import json
from datetime import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from course.models import CourseBase, Category, CourseMarket, Teachplan, CoursePic, CoursePub, TeachplanMedia, \
    TeachplanMediaPub
from course.serializers import CourseBaseSerializer, CategorySerializer, CourseMarketSerializer, TeachplanSerializer, \
    CoursePicSerializer, CourseBasePubSerializer, TeachplanMediaSerializer
from cz_study import settings
from course import helper
from common.paginations import PathPagePagination
from common.exceptions import cast_exception
from common import response_code
from common import sys_dict
from utils import xtime


class CourseBaseViewSet(ModelViewSet):
    queryset = CourseBase.objects.all()
    serializer_class = CourseBaseSerializer
    pagination_class = PathPagePagination
    lookup_url_kwarg = 'course_id'


class CategoryViewSet(GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        queryset = self.get_queryset().filter(parentid=None).first()
        serializer = self.get_serializer(queryset)
        serial_data = serializer.data
        return Response({'children': serial_data.get('children', [])})


class CourseMarketViewSet(ModelViewSet):
    queryset = CourseMarket.objects.all()
    serializer_class = CourseMarketSerializer
    lookup_url_kwarg = 'course_id'

    def update(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        query_set = self.get_queryset().filter(id=course_id).first()
        if query_set:
            return super().update(request, *args, **kwargs)
        else:
            return super().create(request, *args, **kwargs)


class TeachplanViewSet(ModelViewSet):
    queryset = Teachplan.objects.all()
    serializer_class = TeachplanSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(courseid=kwargs['course_id'], parentid=None).first()
        serializer = self.get_serializer(queryset)
        return Response({'children': serializer.data.get('children', [])})

    def create(self, request, *args, **kwargs):
        parentid = request.data.get('parentid')
        courseid = request.data['courseid']
        if not parentid:
            root = Teachplan.objects.filter(grade='1', courseid=courseid).first()
            if not root:
                root = Teachplan.objects.create(pname=courseid, parentid=None, grade='1', courseid=courseid, status='0',
                                                trylearn='0')
            request.data['parentid'] = root.id
            request.data['grade'] = '2'
        else:
            request.data['grade'] = '3'
        return super().create(request, *args, **kwargs)


class CoursePicViewSet(ModelViewSet):
    queryset = CoursePic.objects.all()
    serializer_class = CoursePicSerializer
    lookup_field = 'courseid'
    lookup_url_kwarg = 'course_id'

    def destroy(self, request, *args, **kwargs):
        try:
            resp = super().destroy(request, *args, **kwargs)
            resp.status_code = 200
            return resp
        except Http404:
            cast_exception(response_code.CMS_PAGE_NOTEXISTS)


class CourseSummaryView(APIView):

    def get(self, request, course_id):
        course_base = CourseBase.objects.filter(id=course_id).first()
        course_base_serializer = CourseBaseSerializer(course_base)
        course_pic = CoursePic.objects.filter(courseid=course_id).first()
        course_pic_serializer = CoursePicSerializer(course_pic)
        course_market = CourseMarket.objects.filter(id=course_id).first()
        course_market_serializer = CourseMarketSerializer(course_market)
        teachplan = Teachplan.objects.filter(courseid=course_id, parentid=None).first()
        teachplan_serializer = TeachplanSerializer(teachplan)
        return Response({
            'courseBase': course_base_serializer.data,
            'coursePic': course_pic_serializer.data,
            'courseMarket': course_market_serializer.data,
            'teachplanNode': teachplan_serializer.data,
        })


class CoursePreviewView(APIView):

    def post(self, request, course_id):
        course_base = CourseBase.objects.filter(id=course_id).first()
        page_data = dict(
            siteId=settings.COURSE_PUBLISH['site_id'],
            dataUrl=settings.COURSE_PUBLISH['data_url_pre']+course_id,
            pageName=course_id+'.html',
            pageAlias=course_base.name,
            pageWebPath=settings.COURSE_PUBLISH['page_web_path'],
            pagePhysicalPath=settings.COURSE_PUBLISH['page_physical_path'],
            templateId=settings.COURSE_PUBLISH['template_id'],
            pageType='0',
            pageCreateTime=datetime.now(),
        )
        result = helper.CmsClient().save_cms_page(page_data)
        if not result.success:
            cast_exception(response_code.FAIL)
        url = settings.COURSE_PUBLISH['preview_url'] + result.data.pageId
        return Response({'previewUrl': url})


class CoursePublishView(APIView):

    @staticmethod
    def save_course_pub(course_id):
        # 获取所需数据
        course_base = CourseBase.objects.filter(id=course_id).first()
        course_pic = CoursePic.objects.filter(courseid=course_id).first()
        course_market = CourseMarket.objects.filter(id=course_id).first()
        teachplan = Teachplan.objects.filter(courseid=course_id, grade='1').first()
        # 构造更新字典
        update_data = {}
        update_data.update(**CourseBasePubSerializer(course_base).data)
        update_data.update(**CourseMarketSerializer(course_market).data)
        update_data.update(teachplan=json.dumps(TeachplanSerializer(teachplan).data))
        update_data.update(pic=course_pic.pic if course_pic else '')

        update_data['timestamp'] = datetime.now()
        update_data['pub_time'] = xtime.datetime2timestring(datetime.now())
        # 创建或者更新course_pub数据
        try:
            exists = CoursePub.objects.filter(id=course_id)
            if exists:
                result = exists.update(**update_data)
            else:
                result = CoursePub.objects.create(**update_data)
        except Exception as e:
            print(e)
            return None
        return result

    @staticmethod
    def save_teachplan_media_pub(course_id):
        # 删除已有的媒体发布信息
        TeachplanMediaPub.objects.filter(courseid=course_id).delete()
        # 查询现有的媒体数据
        medias = TeachplanMedia.objects.filter(courseid=course_id)
        # 创建媒体数据对应的媒体发布数据
        for media in medias:
            media_data = TeachplanMediaSerializer(media).data
            media_data['timestamp'] = datetime.now()
            TeachplanMediaPub.objects.create(**media_data)

    def post(self, request, course_id):
        course_base = CourseBase.objects.filter(id=course_id).first()
        if course_base is None:
            cast_exception(response_code.COURSE_NOTEXISTS)
        cms_page = dict(
            siteId=settings.COURSE_PUBLISH['site_id'],
            dataUrl=settings.COURSE_PUBLISH['data_url_pre'] + course_id,
            pageName=course_id + '.html',
            pageAlias=course_base.name,
            pageWebPath=settings.COURSE_PUBLISH['page_web_path'],
            pagePhysicalPath=settings.COURSE_PUBLISH['page_physical_path'],
            templateId=settings.COURSE_PUBLISH['template_id'],
            pageType='0',
            pageCreateTime=datetime.now(),
        )
        result = helper.CmsClient().post_page_quick(cms_page)
        if not result.success:
            cast_exception(response_code.FAIL)
        # 保存课程发布状态
        course_base.status = sys_dict.COURSE_STATUS_PUBLISH
        course_base.save()
        # 保存课程发布信息
        pub_result = self.save_course_pub(course_id)
        if not pub_result:
            cast_exception(response_code.COURSE_PUBLISH_CREATECOURSEPUB_ERROR)
        # 保存课程媒资发布信息
        self.save_teachplan_media_pub(course_id)
        page_url = result.data.pageUrl
        return Response({'pageUrl': page_url})


class SaveMediaView(APIView):

    def post(self, request, *args, **kwargs):
        # 判断teachplanId是否合法
        if not request.data.get('teachplanId'):
            cast_exception(response_code.INVALID_PARAM)
        teachplan_id = request.data.get('teachplanId')
        teachplan = Teachplan.objects.filter(id=teachplan_id).first()
        if teachplan is None:
            cast_exception(response_code.INVALID_PARAM)
        # 判断课程计划grade
        grade = teachplan.grade
        if not grade or grade != '3':
            cast_exception(response_code.COURSE_MEDIA_TEACHPLAN_GRADEERROR)
        # 保存课程计划媒体信息
        media = TeachplanMedia.objects.filter(teachplan_id=teachplan_id).first()
        if media is None:
            media = TeachplanMedia()
        media.courseid = teachplan.courseid
        media.media_id = request.data.get('mediaId')
        media.media_fileoriginalname = request.data.get('mediaFileOriginalName')
        media.media_url = request.data.get('mediaUrl')
        media.teachplan_id = teachplan_id
        media.save()
        return Response()
