from rest_framework.serializers import ListSerializer, ModelSerializer

from apps.dashboard.models import GasesCollected, Sensor


class GasesCollectedListSerializer(ListSerializer):
    def create(self, validated_data):
        collected_gases = [GasesCollected(**item) for item in validated_data]
        return GasesCollected.objects.bulk_create(collected_gases)


class GasesCollectedSerializer(ModelSerializer):
    class Meta:
        model = GasesCollected
        list_serializer_class = GasesCollectedListSerializer
        fields = '__all__'


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
