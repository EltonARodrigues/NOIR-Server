from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('measuring/', views.MeasureView.as_view(), name='nova_medicao'),
    path('dashboard/', views.Graph.as_view(), name='get_context_data'),
    path('dashboard/<uuid:pk>/', views.Graph.as_view(), name='get_context_data'),
    path('', views.SelecaoView.as_view(), name='home'),
]
