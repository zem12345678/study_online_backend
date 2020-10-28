from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.serializers import CharField
from cms.models import CmsSite, CmsTemplate, CmsPage, CmsConfig, CmsConfigModel, SysDictionary, SysDictionaryValue


class CmsSiteSerializer(DocumentSerializer):
    siteId = CharField(source='id', read_only=True)

    class Meta:
        model = CmsSite
        fields = ('siteId', 'siteName')


class CmsTemplateSerializer(DocumentSerializer):
    templateId = CharField(source='id', read_only=True)

    class Meta:
        model = CmsTemplate
        fields = ('templateId', 'templateName')


class CmsPageSerializer(DocumentSerializer):
    pageId = CharField(source='id', read_only=True)

    class Meta:
        model = CmsPage
        fields = ('pageId', 'siteId', 'pageName', 'pageAlias', 'pageWebPath', 'pagePhysicalPath', 'pageType', 'pageStatus', 'pageCreateTime', 'templateId', 'dataUrl')
        read_only_fields = ('pageCreateTime', )


class CmsConfigModelSerializer(DocumentSerializer):
    class Meta:
        model = CmsConfigModel
        fields = ('key', 'name', 'value', 'mapValue', 'url')


class CmsConfigSerializer(DocumentSerializer):
    model = CmsConfigModelSerializer(many=True)

    class Meta:
        model = CmsConfig
        fields = ('id', 'name', 'model')


class SysDictionaryValueSerializer(DocumentSerializer):
    sdId = CharField(source='sd_id')
    sdName = CharField(source='sd_name')
    sdStatus = CharField(source='sd_status')

    class Meta:
        model = SysDictionaryValue
        fields = ('sdId', 'sdName', 'sdStatus')


class SysDictionarySerializer(DocumentSerializer):
    d_value = SysDictionaryValueSerializer(many=True)

    class Meta:
        model = SysDictionary
        fields = ('id', 'd_name', 'd_type', 'd_value')
