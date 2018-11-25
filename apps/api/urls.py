from rest_framework import routers

from .viewsets import GasesCollectedViewSet

router = routers.SimpleRouter()
router.register(r'gases', GasesCollectedViewSet)

urlpatterns = router.urls
