from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'csv', views.ClientViewSetCSV)
router.register(r'json', views.ClientViewSetJSON)


urlpatterns = [
    #path('send', views.get_values, name='getdata'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('setup', views.nova_medicao, name='nova_medicao'),
    path('medicao/', views.Graph.as_view(), name='get_context_data'),
    path('medicao/<int:pk>', views.Graph.as_view(), name='get_context_data'),
    path('', views.SelecaoView.as_view(), name='home'),
    #path('values/', views.values_list),
    path('api/', include(router.urls)),


]
