from functools import partial

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet
from rest_framework_csv.parsers import CSVParser

from apps.dashboard.models import GasesCollected

from .serializers import GasesCollectedSerializer


class GasesCollectedViewSet(ModelViewSet):
    queryset = GasesCollected.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    serializer_class = GasesCollectedSerializer

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if 'text/csv' in self.request.content_type:
            return partial(serializer_class, many=True)

        return serializer_class
