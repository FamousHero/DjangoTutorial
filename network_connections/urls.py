from django.urls import path, re_path

from . import views

app_name = "network_connections"

urlpatterns = [
    path('', views.index, name='index'),
    path('cables/', views.cables, name='cables'),
    path('devices/', views.devices, name='devices'),
    re_path(r'^devices/(?P<mac_address>[0-9a-zA-Z]{12})/$', views.device_details, name='device_details'),
    
  
]