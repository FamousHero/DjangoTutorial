from django.db import transaction
from django.http import HttpResponse

from django.db.models import Q
from ..models import Cable, Device

def delete_cable(request, pk):
    if request.method == "DELETE":
        # must update all connected devices to ports_availiable +1
        # and update port_bitmap (separate function)
        with transaction.atomic():
            cable = Cable.objects.get(pk=pk).delete()
        return HttpResponse(status=204)
    else:
        headers = {
            'Allow': ["Delete"]
        }
        
        return HttpResponse(
            status=405,
            content="Method Not Allowed",
            headers=headers
        )

def delete_device(request, mac_address):
    if request.method == "DELETE":
        # must update all connected devices to ports_available +1
        # and update port_bitmap (separate function)
        with transaction.atomic():
            device = Device.objects.get(mac_address=mac_address)
            connections = Cable.objects.filter(
                Q(device_1=device) | Q(device_2=device)
                )
            print(connections)
            for connection in connections:
                if device == connection.device_1:
                    print("Ok")
                    _update_connections(connection.device_2, connection.port_2)
                elif device == connection.device_2:
                    _update_connections(connection.device_1, connection.port_1)
                    print("Ok 2")

            device.delete()
        return HttpResponse(status=204)
    else:
        headers = {
            'Allow': ["Delete"]
        }
        
        return HttpResponse(
            status=405,
            content="Method Not Allowed",
            headers=headers
        )


def _update_connections(device_to_update: Device, port_number: int):

    device_to_update.ports_available += 1
    port = 1 << (port_number-1)
    print(f"port number: {port_number}")
    # Convert to its signed counterpart
    if port_number == 64:
        port = -port
    
    print(f"port bit value: {port}")
    device_to_update.port_bitmap ^= port
    
    device_to_update.save()