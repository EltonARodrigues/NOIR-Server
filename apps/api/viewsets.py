from functools import partial

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet
from rest_framework_csv.parsers import CSVParser

from apps.dashboard.models import GasesCollected, Sensor

from .serializers import GasesCollectedSerializer, SensorSerializer


class GasesCollectedViewSet(ModelViewSet):
    queryset = GasesCollected.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    serializer_class = GasesCollectedSerializer

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if 'text/csv' in self.request.content_type:
            return partial(serializer_class, many=True)

        return serializer_class


class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
