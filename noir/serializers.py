from .models import Valores
from rest_framework import serializers


class ValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Valores
        fields = ('temperature', 'humidity', 'co' , 'co2', 'mp25', 'id')



class ValuesFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valores
        fields = ('temperature', 'humidity', 'co' , 'co2', 'mp25', 'id')
