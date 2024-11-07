from django.db import models
from django.core.validators import MaxValueValidator, \
    MinValueValidator, MaxLengthValidator, MinLengthValidator

# Create your models here.

class Device(models.Model):
    device_type_choices = {
        "Server": "Server",
        "Hub": "Hub",
        "Switch": "Switch",
        "Router": "Router",
        "Modem": "Modem",
        "Media Converters": "Media Converters",
        "Optical Transceivers": "Optical Transceivers",
    }

    device_type = models.CharField( 
        max_length= 40, 
        choices=device_type_choices,)
    mac_address = models.CharField(max_length=12, validators=[
        MaxLengthValidator(12),
        MinLengthValidator(12)
    ])
    total_ports = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(64)
        ])
    ports_available = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(64)
        ])
    
    port_bitmap = models.BigIntegerField(default=0)

    # Cables connected (foreign Key)


    def __str__(self):
        return f"Server {self.mac_address}"
    

   
class Cable(models.Model):
    cable_type_choices = {
        "CAT5e": "CAT5e",
        "CAT6": "CAT6",
        "CAT6a": "CAT6a",
        "Coaxial": "Coaxial",
        "Single-Mode FIber Optic": "Single-Mode FIber Optic",
        "Multi-Mode Fiber Optic": "Multi-Mode Fiber Optic",
        "OM3/OM4": "OM3/OM4",
        "OM5": "OM5",
        "MTP/MPO": "MTP/MPO",
    }

    cable_length_choices = {
        5: "5ft.",
        8: "8ft.",
        12: "12ft.",
        24: "24ft.",
        36: "36ft.",
        48: "48ft.",
    }

    cable_type = models.CharField(choices=cable_type_choices, max_length=100)
    cable_length = models.IntegerField(choices=cable_length_choices)
    last_validated = models.DateTimeField(auto_now=True)

    device_1 = models.ForeignKey(Device, related_name="device1", on_delete=models.CASCADE)
    port_1 = models.IntegerField(validators=[
        MaxValueValidator(64),
        MinValueValidator(1)
    ])

    device_2 = models.ForeignKey(Device, related_name="device2", on_delete=models.CASCADE)
    port_2 = models.IntegerField(validators=[
        MaxValueValidator(64),
        MinValueValidator(1)
    ])
    def __str__(self):
        return f"Connects Server {self.device_1.mac_address} to {self.device_2.mac_address}\
              on {self.port_1}:{self.port_2}"