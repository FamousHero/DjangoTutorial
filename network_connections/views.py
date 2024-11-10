from django.shortcuts import render
from django.forms.models import model_to_dict

from django.http import HttpResponse, JsonResponse

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import Cable, Device
from .forms import CableForm
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


def items(request, item_type):
    if item_type == "devices":
        items = Device.objects.values()
    elif item_type == "cables":
        items = Cable.objects.values()
    context = {
        "items": items,
        }
    return render(request, "network_connections/item_management.html", context)

# Endpoint, called by js once device is selected, return json of data
def device_details(request, mac_address):
    try:
        device = Device.objects.get(mac_address=mac_address)
        return JsonResponse({"response_str":"status ok, mac_address follows",
                        "mac_address": mac_address,
                        "details": model_to_dict(device)})
    except ObjectDoesNotExist:
        return JsonResponse({ "response_str": "error object not found"})
    
    except MultipleObjectsReturned:
        return JsonResponse({"response_str": "shouldn't happen mac addresses are unique"})
