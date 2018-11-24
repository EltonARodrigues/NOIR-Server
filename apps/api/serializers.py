from rest_framework.serializers import ModelSerializer

from apps.dashboard.models import GasesCollected

class ValuesSerializer(ModelSerializer):
    class Meta:
        model = GasesCollected
        fields = '__all__'
