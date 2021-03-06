# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from treebeard.admin import TreeAdmin

from lizard_security.models import DataSet
from lizard_security.models import PermissionMapper

from ddsc_core import models


class AlarmItemsInline(admin.TabularInline):
    model = models.Alarm_Item
    extra = 1


class AlarmAdmin(admin.ModelAdmin):
    inlines = [AlarmItemsInline]
    list_display = (
        'name',
        'first_born',
        'active_status',
        'single_or_group',
        'frequency',
        'urgency',
        'message_type',
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                ('active_status', ),
                ('single_or_group', 'object_id', ),
                'frequency',
                'urgency',
                'message_type',
                'template',
                'logical_check',
            )
        }),
        ('Details', {
            'classes': ('collapse', ),
            'fields': (
                'description',
                'last_checked',
                'first_born',
                'previous_alarm',
                'date_cr',
            )
        })
    )
    readonly_fields = [
        "last_checked",
        "first_born",
        "previous_alarm",
        "date_cr",
    ]


class AquoModelAdmin(admin.ModelAdmin):
    """ModelAdmin that provides filtering by group."""
    list_display = ("description", "code", "group", "visible", )
    list_filter = ("group", "visible", )
    search_fields = ("code", "description", )

##  def has_add_permission(self, request, obj=None):
##      """Forbid adding any new objects via the Django admin.

##      Currently, only one-way sync is supported. This is just a simple
##      reminder of that fact and by no means a hack-proof solution.

##      """
##      return False


class FolderAdmin(admin.ModelAdmin):
    list_display = ("path", "user", )
    ordering = ("user__username", "path", )
    search_fields = (
        "path",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("label", "user", )
    ordering = ("user__username", "label", )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


class IdMappingAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "timeseries",
        "remote_id",
    )
    list_display = (
        "user",
        "internal_id",
        "external_id",
    )
    list_display_links = (
        "internal_id",
    )
    list_filter = (
        "user",
    )
    ordering = (
        "user__username",
        "timeseries__pk",
    )
    search_fields = (
        "remote_id",
        "timeseries__pk",
        "user__username",
    )

    def internal_id(self, obj):
        return obj.timeseries.pk

    def external_id(self, obj):
        return obj.remote_id

    internal_id.short_description = "Internal timeseries ID"
    external_id.short_description = "External timeseries ID"


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


class TimeseriesSelectionRuleInline(GenericTabularInline):
    model = models.TimeseriesSelectionRule
    extra = 1


class LogicalGroupParentsInline(admin.TabularInline):
    model = models.LogicalGroupEdge
    fk_name = 'child'  # yes 'child', not 'parent'
    verbose_name_plural = "parent groups"
    extra = 1


class LogicalGroupChildrenInline(admin.TabularInline):
    model = models.LogicalGroupEdge
    fk_name = 'parent'  # yes 'parent', not 'child'
    verbose_name_plural = "child groups"
    extra = 1


class LogicalGroupAdmin(admin.ModelAdmin):
    fields = (
        "name", "description",
        ("timeseries", "timeseries_count"),
        "owner", "graph",
    )
    inlines = [
        LogicalGroupParentsInline,
        LogicalGroupChildrenInline,
        TimeseriesSelectionRuleInline,
    ]
    list_display = ("id", "name", "owner", )
    list_display_links = ("name", )
    list_filter = ("owner", )
    raw_id_fields = ("timeseries", )  # fast, but no multiple select...
    readonly_fields = ("timeseries_count", "graph", )
    search_fields = ("=id", "name", )

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
    filter_horizontal = ('data_set', )
    list_display = ('id', 'uuid', 'name', 'description', )
    list_display_links = ('uuid', )
    readonly_fields = ('uuid', )
    search_fields = ('=id', 'name', 'description', 'uuid', )

    fieldsets = (
        (None, {
            'fields': (
                'uuid',
                'name',
                'description',
            )
        }),
        ('Security', {
            'fields': (
                'owner',
                'data_set',
            )
        }),
        ('Aquo DS', {
            'fields': (
                'parameter',
                'unit',
                'reference_frame',
                'compartment',
                'measuring_device',
                'measuring_method',
                'processing_method',
            )
        }),
    )


admin.site.register(models.Alarm, AlarmAdmin)
admin.site.register(models.Alarm_Active)
admin.site.register(models.Alarm_Item)
admin.site.register(models.Compartment, AquoModelAdmin)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.IPAddress, IPAddressAdmin)
admin.site.register(models.IdMapping, IdMappingAdmin)
admin.site.register(models.Location, TreeAdmin)
admin.site.register(models.LocationType, LocationTypeAdmin)
admin.site.register(models.LogRecord, LogRecordAdmin)
admin.site.register(models.LogicalGroup, LogicalGroupAdmin)
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


class PermissionMapperInline(admin.TabularInline):
    model = PermissionMapper
    extra = 1


class DataSetAdmin(admin.ModelAdmin):
    fields = ('name', 'owner', )
    inlines = [TimeseriesSelectionRuleInline, PermissionMapperInline]
    list_display = ('name', 'owner', )
    list_filter = ("owner", )
    search_fields = (
        "name",
        "owner__name",
    )


admin.site.unregister(DataSet)
admin.site.register(DataSet, DataSetAdmin)
