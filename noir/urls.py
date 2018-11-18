from django.urls import path

from . import views


urlpatterns = [
    path('send', views.get_values, name='getdata'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('setup', views.nova_medicao, name='nova_medicao'),
    path('medicao/', views.Graph.as_view(), name='get_context_data'),
    path('medicao/<int:pk>', views.Graph.as_view(), name='get_context_data'),
    path('', views.SelecaoView.as_view(), name='home'),


]
