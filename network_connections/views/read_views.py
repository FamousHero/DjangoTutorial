from django.shortcuts import render
from django.forms.models import model_to_dict

from django.http import JsonResponse

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from ..models import Cable, Device

def items(request, item_type):
    if item_type == "devices":
        items = Device.objects.values()
    elif item_type == "cables":
        items = []
        cables = Cable.objects.all() # Required to pass mac_address vs. default pk
        for cable in cables:         # Allows for easier endpoint access to device_details
            items.append({
                "id": cable.id,
                "device_1_mac": cable.device_1.mac_address,
                "port_1": cable.port_1,
                "cable_type": cable.cable_type,
                "cable_length": cable.cable_length,
                "device_2_mac": cable.device_2.mac_address,
                "port_2": cable.port_2,
                "last_validated": cable.last_validated
            })
    context = {
        "item_type": item_type,
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
