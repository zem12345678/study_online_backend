from rest_framework import serializers
from order.models import CzTaskHis


class CzTaskHisSerializer(serializers.ModelSerializer):

    class Meta:
        model = CzTaskHis
        fields = ('id', 'create_time', 'update_time', 'delete_time', 'task_type', 'mq_exchange', 'mq_routingkey', 'request_body', 'version', 'status', 'errormsg')
