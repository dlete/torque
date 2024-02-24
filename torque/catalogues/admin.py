# Core Django imports
from django.contrib import admin

# This project apps imports
from .models import EthernetPhysicalLayer
from .models import Manufacturer
from .models import Os
from .models import PartNumber
from .models import Supplier
from .models import Transceiver
from .models import TransceiverFormFactor


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']

class OsAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'family', 'version']

class PartNumberAdmin(admin.ModelAdmin):
    list_display = ['part_number', 'description', 'manufacturer']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']

class TransceiverAdmin(admin.ModelAdmin):
    list_display = ['part_number', 'part_number_description', 'form_factor', 
        'type_code', 'part_number_manufacturer']

    def part_number_description(self, obj):
        return obj.part_number.description

    def part_number_manufacturer(self, obj):
        return obj.part_number.manufacturer

class TransceiverFormFactorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


admin.site.register(EthernetPhysicalLayer)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Os, OsAdmin)
admin.site.register(PartNumber, PartNumberAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Transceiver, TransceiverAdmin)
admin.site.register(TransceiverFormFactor, TransceiverFormFactorAdmin)
