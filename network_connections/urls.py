from django.urls import path

from . import views

app_name = "network_connections"

urlpatterns = [
    path('', views.index, name='index'),
  
]