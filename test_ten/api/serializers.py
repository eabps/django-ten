from rest_framework.serializers import ModelSerializer

from test_ten.models import ScheduledService


class ScheduledServiceSerializer(ModelSerializer):
    class Meta:
        model = ScheduledService
        fields = ['id', 'patient', 'date']