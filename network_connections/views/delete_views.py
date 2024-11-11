from django.shortcuts import render, redirect
from django.http import JsonResponse

from ..models import Cable, Device

def delete_cable(request, pk):
    print(f"delete cable pk: {pk}")
    return JsonResponse({'status_code': 200, 'pk': pk})

def delete_device(request, mac_address):
    print(f"delete device mac: {mac_address}")
    return JsonResponse({'status_code': 200, 'mac_address': mac_address})