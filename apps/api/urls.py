from rest_framework import routers

from .viewsets import GasesCollectedViewSet, SensorViewSet

router = routers.SimpleRouter()
router.register(r'gases', GasesCollectedViewSet)
router.register(r'sensors', SensorViewSet)

urlpatterns = router.urls
