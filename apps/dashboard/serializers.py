from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Valores


class ValuesSerializer(ModelSerializer):

    class Meta:
        model = Valores
        fields = ('temperature', 'humidity', 'co' , 'co2', 'mp25', 'id')


'''
class ValuesFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valores
        fields = ('temperature', 'humidity', 'co' , 'co2', 'mp25', 'id')
'''