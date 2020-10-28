from cms.models import CmsTemplate, CmsSite
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_mongoengine.viewsets import ModelViewSet


# Cms Template序列化器
class CmsTemplateSerializer(DocumentSerializer):
    class Meta:
        model = CmsTemplate
        fields = "__all__"


# Cms Template视图集
class CmsTemplateViewSet(ModelViewSet):
    queryset = CmsTemplate.objects
    serializer_class = CmsTemplateSerializer


# Cms Site序列化器
class CmsSiteSerializer(DocumentSerializer):
    class Meta:
        model = CmsSite
        fields = "__all__"


# Cms Site视图集
class CmsSiteViewSet(ModelViewSet):
    queryset = CmsSite.objects
    serializer_class = CmsSiteSerializer

