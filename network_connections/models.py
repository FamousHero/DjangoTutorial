from django.db import models

# Create your models here.

class Device(models.Model):
    # Device number (pk)
    # Device type (Server, Hub, Switch, Router, Modem, 
    #               Media Converters, Optical Transceivers)
    # Total ports
    # Ports available
    # Cables connected (foreign Key)


    def __str__(self):
        return f"Server {self.id}"
    

   
class Cable(models.Model):
    # Device 1 
    # Server 1 port
    # Server 2
    # Server 2 port
    #
    # Cable type
    # Cable length
    # Date connected


    def __str__(self):
        return "Connects Server {} to {} on {}:{}"