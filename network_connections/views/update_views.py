from django.shortcuts import render
from django.forms.models import model_to_dict

from django.http import HttpResponse, JsonResponse

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from ..models import Cable, Device
from ..forms import CableForm

def index(request):
    #TODO: accept post request, validate form, create db entry (transaction based)
    #       validate form -> if valid -> check port_bitmap allows port entered
    if request.method == "POST":
        cable_form = CableForm(request.POST)
        if cable_form.is_valid():
            cable_form = cable_form.cleaned_data
            with transaction.atomic():
                
                # Device 1
                device_1 = cable_form["device_1"]
                device_1_port_bitmap = device_1.port_bitmap
                port_1 = 1 << (cable_form["port_1"] - 1)

                if port_1 & device_1_port_bitmap == 0:
                    device_1_port_bitmap |= port_1
                
                device_1.ports_available -= 1
                device_1.port_bitmap = device_1_port_bitmap
                device_1.save()

                # Device 2
                device_2 = cable_form["device_2"]
                device_2_port_bitmap = device_2.port_bitmap
                port_2 = 1 << (cable_form["port_2"] - 1)

                if port_2 & device_2_port_bitmap == 0:
                    device_2_port_bitmap |= port_2
                
                device_2.ports_available -= 1
                device_2.port_bitmap = device_2_port_bitmap
                device_2.save()

                # Cable
                cable_type = cable_form["cable_type"]
                cable_length = cable_form["cable_length"]
                cable = Cable(cable_type=cable_type, cable_length=cable_length,
                              device_1= device_1, port_1=cable_form["port_1"],
                              device_2=device_2, port_2=cable_form["port_2"])
                cable.save()

            # Start Transaction
                # Update device_1 port_bitmap & decrement av_ports
                # Update device_2 port_bitmap & decrement av_ports
                # Create new Cable using form fields
            # End Transaction

            # Alert Success
            # ref: https://youtu.be/q4jPR-M0TAQ?t=1450
            print("Form submitted & saved")
    
    cable_form = CableForm()
    context = {
        "CableForm": cable_form
    }
    return render(request, "network_connections/cable_form.html", context)
