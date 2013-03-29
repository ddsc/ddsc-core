# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from treebeard.admin import TreeAdmin

from lizard_security.models import DataSet

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


class LogRecordAdmin(admin.ModelAdmin):

    list_display = ("ftime", "host", "level", "message")
    list_filter = ("host", "level")

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
        return obj.time.strftime('%Y-%m-%dT%H:%M:%S.%f')

    ftime.short_description = 'Time'


class TimeseriesInline(admin.TabularInline):
    model = models.Timeseries.data_set.through
    extra = 1


class TimeseriesSelectionRuleInline(GenericTabularInline):
    model = models.TimeseriesSelectionRule
    extra = 1


class LogicalGroupAdmin(admin.ModelAdmin):
    fields = (
        "name", "description",
        ("timeseries", "timeseries_count"),
        "owner", "graph",
    )
    inlines = [TimeseriesSelectionRuleInline]
    list_display = ("name", "owner", )
    list_filter = ("owner", )
    raw_id_fields = ("timeseries", )  # fast, but no multiple select...
    readonly_fields = ("timeseries_count", "graph", )

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


class TimeseriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'uuid', )
    search_fields = ('=id', 'name', 'description', 'uuid', )


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
admin.site.register(models.Timeseries, TimeseriesAdmin)
admin.site.register(models.Unit, AquoModelAdmin)

# Override lizard_security's `DataSet` admin page.


class DataSetAdmin(admin.ModelAdmin):
    fields = ('name', 'owner', )
#   inlines = [TimeseriesSelectionRuleInline]
    inlines = [TimeseriesSelectionRuleInline, TimeseriesInline]
    list_display = ('name', 'owner', )


admin.site.unregister(DataSet)
admin.site.register(DataSet, DataSetAdmin)
