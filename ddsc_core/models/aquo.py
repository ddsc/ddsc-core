# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

"""Models that represent Aquo domain tables.

See: http://domeintabellen-idsw.rws.nl/

The classes below have to match the Java entity classes in ddsc-aquo.
"""

from __future__ import unicode_literals

from django.db import models

APP_LABEL = "ddsc_core"


class AquoModelManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class AquoModel(models.Model):
    """Abstract base class for Aquo domain tables."""
    objects = AquoModelManager()
    code = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=60, unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "{0}".format(self.description)

    def natural_key(self):
        return (self.code, )

    class Meta:
        abstract = True
        app_label = APP_LABEL
        ordering = ['description']


class Compartment(AquoModel):
    """Aquo domain table `Compartiment`."""
    group = models.CharField(max_length=60, null=True)
    numeric_code = models.CharField(max_length=12, null=True)


class MeasuringDevice(AquoModel):
    """Aquo domain table `Meetapparaat`."""
    group = models.CharField(max_length=60, null=True)


class MeasuringMethod(AquoModel):
    """Aquo domain table `Waardebepalingsmethode`."""
    group = models.CharField(max_length=60, null=True)
    titel = models.CharField(max_length=600, null=True)


class Parameter(AquoModel):
    """Aquo domain table `Parameter`."""
    cas_number = models.CharField(max_length=12)
    group = models.CharField(max_length=60)  # Required!
    sikb_id = models.IntegerField(null=True, unique=True)


class ProcessingMethod(AquoModel):
    """Aquo domain table `Waardebewerkingsmethode`."""
    group = models.CharField(max_length=60, null=True)


class ReferenceFrame(AquoModel):
    """Aquo domain table `Hoedanigheid`."""
    group = models.CharField(max_length=60, null=True)


class Unit(AquoModel):
    """Aquo domain table `Eenheid`."""
    group = models.CharField(max_length=60, null=True)
    dimension = models.CharField(max_length=12, null=True)
    conversion_factor = models.CharField(max_length=12, null=True)
