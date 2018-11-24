from rest_framework import routers
from .apis import ClientViewSetCSV, ClientViewSetJSON

router = routers.SimpleRouter()
router.register(r'json', ClientViewSetJSON)
router.register(r'csv', ClientViewSetCSV)

urlpatterns = router.urls
