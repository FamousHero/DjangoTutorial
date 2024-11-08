from django.forms import ModelForm
from .models import Cable

class CableForm(ModelForm):
    class Meta:
        model = Cable
        fields = ["device_1", "port_1", 
                  "device_2", "port_2",
                  "cable_type", "cable_length"]
