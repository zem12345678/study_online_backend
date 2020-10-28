from django.db import models
from rest_framework.serializers import ModelSerializer, ListSerializer, IntegerField, SerializerMethodField
from course.models import CourseBase, Category, CourseMarket, Teachplan, CoursePic, TeachplanMedia


class CourseBaseSerializer(ModelSerializer):

    class Meta:
        model = CourseBase
        fields = ('id', 'name', 'users', 'mt', 'grade', 'studymodel', 'teachmode', 'description', 'st', 'status', 'create_time', 'subtitle', 'serialize', 'target')


class CategoryListSerializer(ListSerializer):
    """
    当Category序列化器取列表数据时，调用该Serializer，完成一些过滤排序的附加功能
    """
    def to_representation(self, data):
        # 对Category数据进行过滤和排序
        data = data.filter(isshow=True).order_by('orderby') if isinstance(data, models.Manager) else data
        return super().to_representation(data)


class Category3Serializer(ModelSerializer):
    class Meta:
        model = Category
        list_serializer_class = CategoryListSerializer
        fields = ('id', 'name', 'label', 'parentid', 'isshow', 'orderby')


class Category2Serializer(ModelSerializer):
    children = Category3Serializer(many=True, read_only=True)

    class Meta:
        model = Category
        list_serializer_class = CategoryListSerializer
        fields = ('id', 'name', 'label', 'parentid', 'isshow', 'orderby', 'children')


class CategorySerializer(ModelSerializer):
    children = Category2Serializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'label', 'parentid', 'isshow', 'orderby', 'children')


class CourseMarketSerializer(ModelSerializer):

    def to_internal_value(self, data):
        if data['expires'] == '':
            data['expires'] = None
        if data['price'] == '':
            data['price'] = None
        return super().to_internal_value(data)

    class Meta:
        model = CourseMarket
        fields = ('id', 'charge', 'valid', 'expires', 'qq', 'price', 'price_old')


class TeachplanListSerializer(ListSerializer):
    """
    当取Teachplan列表数据时，调用该Serializer
    """
    def to_representation(self, data):
        # 对Teachplan中的数据进行排序
        data = data.order_by('orderby') if isinstance(data, models.Manager) else data
        return super().to_representation(data)


class Teachplan3Serializer(ModelSerializer):
    mediaId = SerializerMethodField(method_name='get_media_id')
    mediaFileOriginalName = SerializerMethodField(method_name='get_media_fileoriginalname')

    def get_media_id(self, obj):
        if obj.grade != '3':
            return ''
        media = TeachplanMedia.objects.filter(teachplan_id=obj.id).first()
        if media is None:
            return ''
        return media.media_id

    def get_media_fileoriginalname(self, obj):
        if obj.grade != '3':
            return ''
        media = TeachplanMedia.objects.filter(teachplan_id=obj.id).first()
        if media is None:
            return ''
        return media.media_fileoriginalname

    class Meta:
        model = Teachplan
        list_serializer_class = TeachplanListSerializer
        fields = ('id', 'mediaId', 'mediaFileOriginalName', 'pname', 'parentid', 'grade', 'ptype', 'description',
                  'courseid', 'status', 'orderby', 'timelength', 'trylearn')


class Teachplan2Serializer(ModelSerializer):
    children = Teachplan3Serializer(many=True, read_only=True)

    class Meta:
        model = Teachplan
        list_serializer_class = TeachplanListSerializer
        fields = ('id', 'pname', 'parentid', 'grade', 'ptype', 'description',
                  'courseid', 'status', 'orderby', 'timelength', 'trylearn', 'children')


class TeachplanSerializer(ModelSerializer):
    children = Teachplan2Serializer(many=True, read_only=True)

    class Meta:
        model = Teachplan
        fields = ('id', 'pname', 'parentid', 'grade', 'ptype', 'description',
                  'courseid', 'status', 'orderby', 'timelength', 'trylearn', 'children')


class CoursePicSerializer(ModelSerializer):
    courseId = IntegerField(source='courseid')

    class Meta:
        model = CoursePic
        fields = ('courseId', 'pic')

    def create(self, validated_data):
        pic = CoursePic.find_by_course_id(validated_data['courseid'])
        if pic:
            return super().update(CoursePic(), validated_data)
        else:
            return super().create(validated_data)


class CourseBasePubSerializer(ModelSerializer):
    class Meta:
        model = CourseBase
        fields = ('id', 'name', 'users', 'mt', 'st', 'grade', 'studymodel', 'teachmode', 'description')


class TeachplanMediaSerializer(ModelSerializer):
    class Meta:
        model = TeachplanMedia
        fields = ('teachplan_id', 'media_id', 'media_fileoriginalname', 'media_url', 'courseid')
