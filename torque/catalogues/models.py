'''
Notes on Django model fields:
https://docs.djangoproject.com/en/1.11/ref/models/fields/#unique

null, default is False
blank, default is False

unique. When unique is True, you don’t need to specify db_index, 
because unique implies the creation of an index.

To do:

Notes on OneToOne:
https://github.com/encode/django-rest-framework/issues/720
https://github.com/encode/django-rest-framework/issues/5135
'''
        
# Core Django imports
from django.db import models


class EthernetPhysicalLayer(models.Model):
    name = models.CharField(max_length = 255,
        unique = True, 
        verbose_name = "Ethernet Physical Layer Specification"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Ethernet Physical Layer Specification"
        verbose_name_plural = "Ethernet Physical Layer Specifications"

    def __str__(self):
        """
        String for representing the EthernetPhysicalLayer object (in Admin site etc.)
        """
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length = 255, 
        unique = True, 
        verbose_name = "Manufacturer name"
    )
    abbreviation = models.CharField(max_length=50, 
        null = True,
        blank = True,
        verbose_name = "Manufacturer abbreviation"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Manufacturer, OEM (Original Equipment Manufacturer)"
        verbose_name_plural = "Manufacturers, OEMs (Original Equipment Manufacturers)"

    def __str__(self):
        """
        String for representing the Manufacturer object (in Admin site etc.)
        """
        return self.name


class PartNumber(models.Model):
    '''
    We should be getting these records from assetdb.heanet.ie
    This table should not be filled manually.
    '''
    part_number = models.CharField(max_length = 255,
        unique = True, 
        verbose_name = "Part Number"
    )
    description = models.CharField(max_length = 255, 
        null = True,
        blank = True
    )
    manufacturer = models.ForeignKey(
        Manufacturer, 
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        verbose_name = "Manufacturer"
    )
    
    class Meta:
        ordering = ['part_number']
        verbose_name = "Part Number"
        verbose_name_plural = "Part Numbers"

    def __str__(self):
        """
        String for representing the PartNumber object (in Admin site etc.)
        """
        return self.part_number


class Supplier(models.Model):
    '''
    We should be getting these records from assetdb.heanet.ie
    This table should not be filled manually.
    '''
    name = models.CharField(max_length = 255, 
        unique = True
    )
    abbreviation = models.CharField(max_length = 50, 
        unique = True
    )

    def __str__(self):
        """
        String for representing the Supplier object (in Admin site etc.)
        """
        return self.name


class TransceiverFormFactor(models.Model):
    name = models.CharField(max_length = 255,
        unique = True, 
        verbose_name = "Form factor"
    )
    description = models.CharField(max_length = 255, 
        null = True,
        blank = True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Transceiver Form Factor"
        verbose_name_plural = "Transceiver Form Factors"

    def __str__(self):
        """
        String for representing the TransceiverFormFactor object (in Admin site etc.)
        """
        return self.name


class Transceiver(models.Model):
    '''
    Originally, part_number was setup as ForeignKey + unique=True, but Django
	migrations did throw the message below. As a result, did change to 
	OneToOneField. Note though that once a relationship is set to OneToOneField
	the there is no more an "id" field in this model. The database table will 
	NOT have an id field.
    WARNINGS:
    catalogues.Transceiver.part_number: (fields.W342) Setting unique=True on a
    ForeignKey has the same effect as using a OneToOneField.
    HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.

    #part_number = models.ForeignKey(PartNumber,
    #    unique = True,
    #    verbose_name = "Part Number"
    #)
    '''
    part_number = models.OneToOneField(
        PartNumber,
        on_delete=models.CASCADE,
        #primary_key=True,
        primary_key=False,
        verbose_name = "Part Number"
    )
    form_factor = models.ForeignKey(
        TransceiverFormFactor, 
        on_delete=models.CASCADE,
        blank = True, 
        null = True,
        verbose_name = "Form Factor"
    )
    type_code = models.CharField(max_length = 255,
        null = True,
        blank = True,
        verbose_name = "Setting for Type/Cable Type configuration"
    )
    powerbudget = models.DecimalField(max_digits = 4, decimal_places = 2,
        null = True,
        blank = True,
        verbose_name = 
            "Power budget, delta between Transmit Min. and Receive Min."
    )
    receive_min = models.DecimalField(max_digits = 4, decimal_places = 2,
        null = True,
        blank = True,
        verbose_name = "Minimum dBm tolerated on receive"
    )
    receive_max = models.DecimalField(max_digits = 4, decimal_places = 2,
        null = True,
        blank = True,
        verbose_name = "Maximum dBm tolerated on receive"
    )

    class Meta:
        ordering = ['part_number']
        verbose_name = "Transceiver"
        verbose_name_plural = "Transceivers"

    def __str__(self):
        """
        String for representing the Transceiver object (in Admin site etc.)
        """
        return self.part_number.part_number



class Os(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name = "Manufacturer"
    )
    family = models.CharField(max_length = 255,
        verbose_name = "OS Family"
    )
    version = models.CharField(max_length = 255,
        verbose_name = "Version"
    )

    class Meta:
        ordering = ['manufacturer']
        verbose_name = "Operating Sytem"
        verbose_name_plural = "Operating Systems"

    def __str__(self):
        """
        String for representing the Os object (in Admin site etc.)
        """
        return self.manufacturer.name
