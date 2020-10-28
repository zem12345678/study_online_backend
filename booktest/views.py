from rest_framework_mongoengine.viewsets import ModelViewSet
from booktest.models import BookInfo, HeroInfo
from booktest.serializers import BookInfoSerializer, HeroInfoSerializer
from rest_framework.exceptions import APIException
from common import exceptions, response_code


class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def list(self, request, *args, **kwargs):
        # exceptions.cast_exception(response_code.FAIL)
        return super().list(request, *args, **kwargs)


class HeroInfoViewSet(ModelViewSet):
    queryset = HeroInfo.objects
    serializer_class = HeroInfoSerializer
