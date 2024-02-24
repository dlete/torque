# Core Django imports
from django.shortcuts import render

# This project apps imports
from catalogues.models import Manufacturer
from catalogues.models import PartNumber
from catalogues.models import Transceiver
from catalogues.models import TransceiverFormFactor


def transceiver_all(request):
    context = {'bodymessage': "Transceivers catalogue"}
    context['transceiver_all'] = Transceiver.objects.all()
    return render(request, 'catalogues/transceiver_all.html', context)
