# Core Django imports
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# This project apps imports
from inventories.models import Circuit
from inventories.models import Ne


def circuit_list(request):
    context = {'bodymessage': "Circuits inventory"}
    context['circuit_list'] = Circuit.objects.all()
    return render(request, 'inventories/circuit_list.html', context)


def index(request):
    # take this as the landing page. For the moment redirect. 
    # At some point, a very simple page with 1-2 choices? dropdown?
    return redirect(ne_list)


def ne_list(request):
    context = {'bodymessage': "Inventory -> Index"}

    '''
    # This section works when settings DEBUG=True, but NOT when False!!!
    # maybe related to serving static files in productin??? Whitenoise package?
    import os, random
    gif_random = random.choice(os.listdir('static/gif'))
    print(gif_random)
    context['gif_random'] = gif_random
    '''
    import os, random
    from datetime import datetime
    random.seed(datetime.now())

    dir_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(dir_parent)
    dir_gif = os.path.join(dir_parent, 'static/gif')
    #print(dir_gif)
    gif_random = random.choice(os.listdir(dir_gif))
    #print(gif_random)
    context['gif_random'] = gif_random

    context['ne_all'] = Ne.objects.all()
    return render(request, 'inventories/ne_list.html', context)


def ne_detail(request, pk):
    context = {'bodymessage': "Inventory -> NE detail"}
    ne = get_object_or_404(Ne, pk=pk)
    context = {'bodymessage': "Details for " + ne.fqdn }
    context['ne'] = ne

    nni_neighbors = ne.nni_neighbors.all()
    context['nni_neighbors'] = nni_neighbors

    '''
    # for graphing, work in progress
    ne_params = get_me_ne_attributes(ne_id)
    nni_neighbors_expected = ne_params['nni_neighbors']
    print("nni_neighbors_expected")
    print(nni_neighbors_expected)
    hostname = ne.fqdn.split('.')[0]
    print("hostname")
    print(hostname)
    from core.utils import graph_ne_nni
    graph_ne_nni.graph_ne_nni(hostname, nni_neighbors_expected)
    context['img_name'] = "nnis_" + hostname + ".svg"
    '''

    ''' to show a random gif while the audit report loads '''
    import os, random
    from datetime import datetime
    random.seed(datetime.now())
    dir_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_gif = os.path.join(dir_parent, 'static/gif')
    gif_random = random.choice(os.listdir(dir_gif))
    context['gif_random'] = gif_random

    return render(request, 'inventories/ne_detail.html', context)
