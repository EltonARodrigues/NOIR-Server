from functools import partial

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet
from rest_framework_csv.parsers import CSVParser
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.models import GasesCollected, Sensor
from rest_framework.authentication import TokenAuthentication
from .serializers import GasesCollectedSerializer, SensorSerializer, SensorsSerializer
from django.contrib.auth.models import User


import jwt
from rest_framework_jwt.utils import jwt_payload_handler


class GasesCollectedViewSet(ModelViewSet):
    queryset = GasesCollected.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    serializer_class = GasesCollectedSerializer

    def get_queryset(self):
        queryset = GasesCollected.objects.none()

        sensors = Sensor.objects.filter(author=self.request.user)
        for sensor in sensors:
            queryset |= GasesCollected.objects.filter(sensor=sensor)
            
        print(queryset)
        return queryset


class SensorsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Sensor.objects.all()
    serializer_class = SensorsSerializer
    
    def get_queryset(self):
        queryset = Sensor.objects.filter(author= self.request.user)
        return queryset


class SensorViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def get_queryset(self):
        queryset = Sensor.objects.filter(author= self.request.user)
        return queryset

