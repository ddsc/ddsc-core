# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib import admin
from treebeard.admin import TreeAdmin

from ddsc_core import models

admin.site.register(models.Location, TreeAdmin)


class AquoModelAdmin(admin.ModelAdmin):
    """ModelAdmin that provides filtering by group."""
    list_filter = ('group', )

admin.site.register(models.Compartment, AquoModelAdmin)
admin.site.register(models.MeasuringDevice, AquoModelAdmin)
admin.site.register(models.MeasuringMethod, AquoModelAdmin)
admin.site.register(models.Parameter, AquoModelAdmin)
admin.site.register(models.ProcessingMethod, AquoModelAdmin)
admin.site.register(models.ReferenceFrame, AquoModelAdmin)
admin.site.register(models.Unit, AquoModelAdmin)
admin.site.register(models.Folder, admin.ModelAdmin)
admin.site.register(models.IPAddress, admin.ModelAdmin)
