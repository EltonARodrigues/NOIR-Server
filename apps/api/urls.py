from rest_framework import routers

from .viewsets import GasesCollectedViewSet, SensorsViewSet, SensorViewSet

router = routers.SimpleRouter()
router.register(r'gases', GasesCollectedViewSet)
router.register(r'sensors', SensorsViewSet)
router.register(r'sensor', SensorViewSet)

urlpatterns = router.urls
