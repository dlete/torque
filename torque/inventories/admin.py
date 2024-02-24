# Core Django imports
from django.contrib import admin

# This project apps imports
from .models import Circuit
from .models import Ne
from .models import OsCredential


class CircuitAdmin(admin.ModelAdmin):
    list_display = [
        'supplier', 
        'circuit_id',
        'a_end_description',
        'b_end_description'
    ]

class NeAdmin(admin.ModelAdmin):
    list_display = [
        'fqdn',
        'os_credential'
    ]

    """
    Adding a ManyToManyField to this list will instead use a nifty unobtrusive 
    JavaScript “filter” interface that allows searching within the options.
    The unselected and selected options appear in two boxes side by side.
    See filter_vertical to use a vertical interface.
    """
    filter_horizontal = ('nni_neighbors',)

admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Ne, NeAdmin)
admin.site.register(OsCredential)
