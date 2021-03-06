from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('setup/', views.MeasureView.as_view(), name='nova_medicao'),
    path('medicao/', views.Graph.as_view(), name='get_context_data'),
    path('medicao/<uuid:pk>/', views.Graph.as_view(), name='get_context_data'),
    path('', views.SelecaoView.as_view(), name='home'),
    path('teste/', views.SelecaoView2.as_view()),
]
