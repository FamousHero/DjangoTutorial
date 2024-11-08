from django.shortcuts import render
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
    cable_form = CableForm()
    context = {
        "CableForm": cable_form
    }
    return render(request, "network_connections/cable_form.html", context)