from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
#from rest_framework.authtoken.views import obtain_auth_token  
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.dashboard.urls')),
    path('api/', include('apps.api.urls')),
    path('api/auth', obtain_jwt_token),
    path('api/auth-refresh/', refresh_jwt_token),
]
