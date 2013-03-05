# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib import admin
from treebeard.admin import TreeAdmin

from ddsc_core import models


class AquoModelAdmin(admin.ModelAdmin):
    """ModelAdmin that provides filtering by group."""
    list_filter = ("group", )

    def has_add_permission(self, request, obj=None):
        """Forbid adding any new objects via the Django admin.

        Currently, only one-way sync is supported. This is just a simple
        reminder of that fact and by no means a hack-proof solution.

        """
        return False


class LocationTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ("locations", )


class LogicalGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("timeseries", )
    list_display = ("name", "owner")
    list_filter = ("owner", )
    readonly_fields = ("graph", )

    def get_readonly_fields(self, request, obj=None):
        """Return a tuple of read-only fields.

        Allowing one to change the owner of a logical group opens a can of
        worms, because this may result in illegal edges (i.e. edges that
        connect nodes having different owners). For that reason, the
        owner cannot be changed afterwards.

        """
        if obj is None:
            # Adding a LogicalGroup
            return self.readonly_fields
        else:
            # Changing a LogicalGroup
            return ("owner", ) + self.readonly_fields


class LogRecordAdmin(admin.ModelAdmin):

    exclude = (
        "time",
    )

    readonly_fields = (
        "ftime",
        "host",
        "level",
        "message",
        "source",
        "line",
    )

    def ftime(self, obj):
        return obj.time.strftime('%Y-%M-%dT%H:%M:%S.%f')

    ftime.short_description = 'Time'


admin.site.register(models.Alarm)
admin.site.register(models.Alarm_Item)
admin.site.register(models.Compartment, AquoModelAdmin)
admin.site.register(models.Folder)
admin.site.register(models.IPAddress)
admin.site.register(models.IdMapping)
admin.site.register(models.Location, TreeAdmin)
admin.site.register(models.LocationType, LocationTypeAdmin)
admin.site.register(models.LogRecord, LogRecordAdmin)
admin.site.register(models.LogicalGroup, LogicalGroupAdmin)
admin.site.register(models.LogicalGroupEdge)
admin.site.register(models.Manufacturer)
admin.site.register(models.MeasuringDevice, AquoModelAdmin)
admin.site.register(models.MeasuringMethod, AquoModelAdmin)
admin.site.register(models.Parameter, AquoModelAdmin)
admin.site.register(models.ProcessingMethod, AquoModelAdmin)
admin.site.register(models.ReferenceFrame, AquoModelAdmin)
admin.site.register(models.Source)
admin.site.register(models.Timeseries)
admin.site.register(models.Unit, AquoModelAdmin)
