'''
Notes on Django model fields:
https://docs.djangoproject.com/en/1.11/ref/models/fields/#unique

null, default is False
blank, default is False

unique. When unique is True, you don’t need to specify db_index,
because unique implies the creation of an index.

To do:
'''

# Core Django imports
from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns



class Circuit(models.Model):
    supplier = models.ForeignKey(
        'catalogues.supplier',
        on_delete = models.PROTECT,
        related_name = "supplier",
    )
    circuit_id = models.CharField(max_length = 50, 
        unique = True,
        verbose_name = "Circuit ID",
        help_text = "Unique identifier provided by the supplier for this circuit. Has to be unique across all the circuits in the database."
    )
    a_end_description = models.CharField(max_length = 255,
        blank = True
    )
    b_end_description = models.CharField(max_length = 255,
        blank = True
    )
    circuit_type = models.CharField(max_length = 255, 
        blank = True
    )
    circuit_info = models.CharField(max_length = 255,
        blank = True
    )

    def __str__(self):
        """
        String for representing the Circuit object (in Admin site etc.)
        """
        return self.circuit_id


class OsCredential(models.Model):
    username = models.CharField(max_length = 64, 
        unique = True,
        help_text = "Username to authenticate with in this NE."
    )
    password = models.CharField(max_length=64,
        help_text = "Password to authenticate with in this NE."
    )

    class Meta:
        """
        Default ordering of records returned when querying the model.
        """
        ordering = ['username']
        verbose_name = "Operating System credentials"

    def __str__(self):
        """
        String for representing the OsCredential object (in Admin site etc.)
        """
        return self.username


class Ne(models.Model):
    fqdn = models.CharField(max_length = 255,
        unique = True,
        verbose_name = "FQDN",
        help_text = "As {hostname}.{domain/sub-domain}.{tld}; e.g. 'core1-lim1.nn.hea.net'."
    )
    os_credential = models.ForeignKey(
        OsCredential,
        on_delete = models.SET_NULL, 
        null = True,
        blank = True, 
        verbose_name = "OS Credentials",
        help_text = "Username to authenticate with in this NE."
    )
    # when doing: python manage.py makemigrations
    # WARNINGS:
    # inventory.Ne.nni_neighbor: (fields.W340) null has no effect 
    # on ManyToManyField.
    nni_neighbors = models.ManyToManyField(
        'self', 
        blank = True,
        verbose_name = 'NNI neighbors',
        help_text = "What other NE is this NE connected to. There is only need to create the relationship in one of the NE, then the system will automatically create the reverse relationship."
    )

    class Meta:
        """
        Default ordering of records returned when querying the model.
        """
        ordering = ['fqdn']
        verbose_name = "Network Element"
        verbose_name_plural = "Network Elements"

    def __str__(self):
        """
        String for representing the Ne object (in Admin site etc.)
        """
        return self.fqdn

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Ne.

        When this method is defined in model.py, Django automatically adds a 
        "View on Site" button to the model's record editing screens in the 
        Admin site.
        """
        return reverse('inventories:ne_detail', args=[str(self.id)])


'''
class AdminStatus(models.Model):
    status = models.CharField(max_length = 255,
        unique = True,
        verbose_name = "Operational status"
    )

    class Meta:
        ordering = ['status']
        verbose_name = "Status"
        verbose_name = "Statuses"

    def __str__(self):
        return self.fqdn
'''
