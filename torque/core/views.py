# Core Django imports
from django.shortcuts import render


def about(request):
    context = {'bodymessage': "About this project"}
    return render(request, 'core/about.html', context)

def features(request):
    context = {
        'bodymessage':
            "These are the items the tool will audit."
    }
    return render(request, 'core/features.html', context)

def known_bugs(request):
    context = {
        'bodymessage':
            "These are the known bugs or problems at this point in time."
    }
    return render(request, 'core/known_bugs.html', context)
