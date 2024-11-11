from django.urls import path, re_path

from .views import create_views, delete_views, read_views, update_views

app_name = "network_connections"

urlpatterns = [
    path('', create_views.index, name='index'),

    re_path(r'^(?P<item_type>cables|devices)/$', 
            read_views.items, name='items'),
    re_path(r'^devices/(?P<mac_address>[0-9a-zA-Z]{12})/$', 
            read_views.device_details, name='device_details'),
    
    path('cables/<int:pk>/delete', delete_views.delete_cable, name='delete_cable'),
    path('devices/<slug:mac_address>/delete', delete_views.delete_device, name='delete_device')
  
]