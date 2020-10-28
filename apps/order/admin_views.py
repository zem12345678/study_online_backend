from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from order.models import CzTask, CzTaskHis


class CzTaskSerializer(ModelSerializer):
    class Meta:
        model = CzTask
        fields = '__all__'


class CzTaskHisSerializer(ModelSerializer):
    class Meta:
        model = CzTaskHis
        fields = '__all__'


class CzTaskViewSet(ModelViewSet):
    queryset = CzTask.objects.all()
    serializer_class = CzTaskSerializer


class CzTaskHisViewSet(ModelViewSet):
    queryset = CzTaskHis.objects.all()
    serializer_class = CzTaskHisSerializer
