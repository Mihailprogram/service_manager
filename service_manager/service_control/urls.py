from django.urls import path
from . import views
from .api import (
    ServiceStatusAPIView,
    AccessStatusAPIView,
    AccessControlAPIView,
    ServiceControlAPIView,
    ToggleAccessAPIView
)

urlpatterns = [
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/status/', ServiceStatusAPIView.as_view(), name='api_status'),
    path('api/access/', AccessStatusAPIView.as_view(), name='api_access_status'),
    path('api/access/<str:action>/', AccessControlAPIView.as_view(), name='api_access_control'),
    path('api/control/<str:action>/', ServiceControlAPIView.as_view(), name='api_service_control'),
    path('api/toggle-access/', ToggleAccessAPIView.as_view(), name='api_toggle_access'),
]