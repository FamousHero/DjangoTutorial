from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import CableForm

from django.db import transaction

from .models import Cable
# Create your views here.

# Template view should have a form with 
#   Server 1
#   Port 1
#   Server 2
#   Port 2
#  
#   Cable type (Copper: CAT5e, CAT6, CAT6a, coaxial, 
#               Fiber Optic: Single-Mode, Mult-Mode Fiber, OM3/OM4, OM5, MTP/MPO )
#       Ref: https://www.networkcablingservices.com/a-comprehensive-guide-to-data-center-cabling/

# Cable Length
#

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

#TODO: update page, delete page, create page(devices)


def devices(request):
    return HttpResponse("Device Page")

# Endpoint, called by js once device is selected, return json of data
def device_details(request, mac_address):
    return JsonResponse({"response_str":"status ok, mac_address follows",
                        "mac_address": mac_address})