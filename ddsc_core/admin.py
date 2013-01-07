# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib import admin
from treebeard.admin import TreeAdmin

from ddsc_core import models


class AquoModelAdmin(admin.ModelAdmin):
    """ModelAdmin that provides filtering by group."""
    list_filter = ("group", )


class LocationGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("locations", )


class LogicalGroupAdmin(admin.ModelAdmin):
    readonly_fields = ("graph", )

admin.site.register(models.Compartment, AquoModelAdmin)
admin.site.register(models.Folder)
admin.site.register(models.IPAddress)
admin.site.register(models.Location, TreeAdmin)
admin.site.register(models.LocationGroup, LocationGroupAdmin)
admin.site.register(models.LogicalGroup, LogicalGroupAdmin)
admin.site.register(models.LogicalGroupEdge)
admin.site.register(models.MeasuringDevice, AquoModelAdmin)
admin.site.register(models.MeasuringMethod, AquoModelAdmin)
admin.site.register(models.Parameter, AquoModelAdmin)
admin.site.register(models.ProcessingMethod, AquoModelAdmin)
admin.site.register(models.ReferenceFrame, AquoModelAdmin)
admin.site.register(models.Unit, AquoModelAdmin)
