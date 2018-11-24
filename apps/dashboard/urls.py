from django.urls import include, path
from rest_framework import routers

from . import views

#from rest_framework_swagger.views import get_swagger_view
#from rest_framework.schemas import get_schema_view
#from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

ROUTER = routers.SimpleRouter()
ROUTER.register(r'json', views.ClientViewSetJSON)
ROUTER.register(r'csv', views.ClientViewSetCSV)

#schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('setup', views.MeasureView.as_view(), name='nova_medicao'),
    path('medicao/', views.Graph.as_view(), name='get_context_data'),
    path('medicao/<uuid:pk>', views.Graph.as_view(), name='get_context_data'),
    path('', views.SelecaoView.as_view(), name='home'),
    path('api/', include(ROUTER.urls)),
    path('teste', views.SelecaoView2.as_view()),
]
