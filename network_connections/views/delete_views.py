from django.http import HttpResponse

from ..models import Cable, Device

def delete_cable(request, pk):
    if request.method == "DELETE":
        Cable.objects.get(pk=pk).delete()
        return HttpResponse(status_code=204)
    else:
        headers = {
            'Allow': ["Delete"]
        }
        
        return HttpResponse(
            status_code=405,
            content="Method Not Allowed",
            headers=headers
        )

def delete_device(request, mac_address):
    if request.method == "DELETE":
        Device.objects.get(mac_address=mac_address).delete()
        return HttpResponse(status_code=204)
    else:
        headers = {
            'Allow': ["Delete"]
        }
        
        return HttpResponse(
            status_code=405,
            content="Method Not Allowed",
            headers=headers
        )