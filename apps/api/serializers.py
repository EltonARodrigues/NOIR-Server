from rest_framework.serializers import ModelSerializer, ListSerializer

from apps.dashboard.models import GasesCollected


class GasesCollectedListSerializer(ListSerializer):
    def create(self, validated_data):
        collected_gases = [GasesCollected(**item) for item in validated_data]
        return GasesCollected.objects.bulk_create(collected_gases)


class GasesCollectedSerializer(ModelSerializer):
    class Meta:
        model = GasesCollected
        list_serializer_class = GasesCollectedListSerializer
        fields = '__all__'
