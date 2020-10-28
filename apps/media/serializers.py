from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.serializers import CharField
from media.models import MediaFile


class MediaFileSerializer(DocumentSerializer):

    class Meta:
        model = MediaFile
        fields = '__all__'
