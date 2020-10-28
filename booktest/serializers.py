from rest_framework_mongoengine.serializers import DocumentSerializer
from booktest.models import BookInfo, HeroInfo


class BookInfoSerializer(DocumentSerializer):

    class Meta:
        model = BookInfo
        fields = '__all__'


class HeroInfoSerializer(DocumentSerializer):

    class Meta:
        model = HeroInfo
        fields = '__all__'
