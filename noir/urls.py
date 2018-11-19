from django.urls import path, include
from . import views
from rest_framework import routers
#from rest_framework_swagger.views import get_swagger_view
#from rest_framework.schemas import get_schema_view
#from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

router = routers.SimpleRouter()
router.register(r'json', views.ClientViewSetJSON)
router.register(r'csv', views.ClientViewSetCSV)

#schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('setup', views.nova_medicao, name='nova_medicao'),
    path('medicao/', views.Graph.as_view(), name='get_context_data'),
    path('medicao/<int:pk>', views.Graph.as_view(), name='get_context_data'),
    path('', views.SelecaoView.as_view(), name='home'),
    #path('api/', schema_view),
    path('api/', include(router.urls)),



]
