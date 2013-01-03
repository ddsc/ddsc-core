# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from treebeard.mp_tree import MP_Node

from cassandralib.models import CassandraDataStore
from cassandralib.models import INTERNAL_TIMEZONE
from ddsc_core import manager
from ddsc_core.models import aquo
from lizard_security.models import DataSet

APP_LABEL = "ddsc_core"
CASSANDRA = getattr(settings, 'CASSANDRA', {})


class DataStore(CassandraDataStore):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kw):
        super(DataStore, self).__init__(
            CASSANDRA['servers'],
            CASSANDRA['keyspace'],
            CASSANDRA['batch_size'],
        )


class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = APP_LABEL


class Location(BaseModel, MP_Node):
    """Location of a timeseries.

    Locations can be nested. The resulting tree is encoded via the materialized
    path algorithm and is best managed via the API provided by treebeard or
    the Django admin interface to keep it consistent.

    """
    objects = manager.LocationManager()

    # TODO: what's the purpose of this code field?
    # Is it to be used for PI-XML's locationId?
    # That does not make much sense to me...
    code = models.CharField(
        unique=True,
        max_length=12,
        help_text="code for identification of location"
    )
    name = models.CharField(
        max_length=80,
        help_text="name of location"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='optional description for timeseries'
    )

    #relative_location
    point_geometry = models.PointField(dim=3, null=True, blank=True)
    real_geometry = models.GeometryField(dim=3, null=True, blank=True)
    geometry_precision = models.FloatField(
        null=True,
        blank=True,
        help_text='precision in meters of location'
    )

    def __unicode__(self):
        return self.name


class LocationGroup(BaseModel):
    name = models.CharField(max_length=80)
    locations = models.ManyToManyField(
        Location,
        blank=True,
        related_name='location_groups'
    )

    def __unicode__(self):
        return self.name


class Timeseries(BaseModel):
    objects = manager.TimeseriesManager()

    class ValueType:
        INTEGER = 0
        FLOAT = 1
        TEXT = 4
        IMAGE = 5
        GEO_REMOTE_SENSING = 7
        MOVIE = 8
        FILE = 10

    VALUE_TYPE = (
        (ValueType.INTEGER, 'integer'),
        (ValueType.FLOAT, 'float'),
        (ValueType.TEXT, 'text'),
        (ValueType.IMAGE, 'image'),
        (ValueType.GEO_REMOTE_SENSING, 'georeferenced remote sensing'),
        (ValueType.MOVIE, 'movie'),
        (ValueType.FILE, 'file'),
    )

    class TimeseriesType:
        HISTORICAL = 0
        SIMULATED_FORECAST = 1
        SIMULATED_HISTORICAL = 2

    TIMESERIES_TYPE = (
        (TimeseriesType.HISTORICAL, 'historical'),
        (TimeseriesType.SIMULATED_FORECAST, 'simulated forecast'),
        (TimeseriesType.SIMULATED_HISTORICAL, 'simulated historical'),
    )

    code = models.CharField(
        unique=True,
        max_length=64,
        help_text="generated code for timeseries identification"
    )
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text='optional name for timeseries'
    )
    description = models.TextField(
        default="",
        blank=True,
        help_text='optional description for timeseries'
    )
    data_set = models.ManyToManyField(DataSet, related_name='timeseries')

    supplying_system = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='timeseries'
    )

    #type information
    value_type = models.SmallIntegerField(default=1, choices=VALUE_TYPE)

    #references to other models
    #owner = models.ForeignKey('DataOwner')
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        related_name='timeseries'
    )

    # References to Aquo Domain Tables
    parameter = models.ForeignKey(aquo.Parameter, null=True, blank=True)
    unit = models.ForeignKey(aquo.Unit, null=True, blank=True)
    reference_frame = models.ForeignKey(aquo.ReferenceFrame, null=True, blank=True)
    compartment = models.ForeignKey(aquo.Compartment, null=True, blank=True)
    measuring_device = models.ForeignKey(aquo.MeasuringDevice, null=True, blank=True)
    measuring_method = models.ForeignKey(aquo.MeasuringMethod, null=True, blank=True)
    processing_method = models.ForeignKey(aquo.ProcessingMethod, null=True, blank=True)

    first_value_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        help_text='timestamp of first value'
    )

    latest_value_number = models.FloatField(null=True, blank=True)
    latest_value_text = models.TextField(
        null=True,
        blank=True,
        help_text='latest value in case of a text, image or file type '
                  '(image and file is a reference to the file location'
    )
    latest_value_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        help_text='timestamp of latest value'
    )

    def latest_value(self):
        if self.value_type == Timeseries.ValueType.INTEGER \
                or self.value_type == Timeseries.ValueType.FLOAT:
            return self.latest_value_number
        if self.value_type == Timeseries.ValueType.TEXT \
                or self.value_type == Timeseries.ValueType.IMAGE:
            return self.latest_value_text
        return None

    def get_events(self, start=None, end=None, filter=None):
        if end is None:
            end = datetime.now()
        if start is None:
            start = end + relativedelta(years=-5)
        if filter is None:
            filter = ['value', 'flag']

        start = INTERNAL_TIMEZONE.localize(start)
        end = INTERNAL_TIMEZONE.localize(end)

        if start < self.first_value_timestamp:
            start = self.first_value_timestamp
        if end > self.latest_value_timestamp:
            end = self.latest_value_timestamp

        store = DataStore()
        return store.read('events', self.code, start, end, params=filter)

    def set_events(self, df):
        for timestamp, row in df.iterrows():
            self.set_event(timestamp, row)

    def set_event(self, timestamp, row):
        store = DataStore()
        store.write_row('events', self.code, timestamp, row)
        if 'value' in row:
            if not self.latest_value_timestamp \
                    or self.latest_value_timestamp < timestamp:
                if self.value_type == Timeseries.ValueType.INTEGER \
                        or self.value_type == Timeseries.ValueType.FLOAT:
                    self.latest_value_number = row['value']
                elif self.value_type == Timeseries.ValueType.TEXT \
                        or self.value_type == Timeseries.ValueType.IMAGE:
                    self.latest_value_text = row['value']
                self.latest_value_timestamp = timestamp
            if not self.first_value_timestamp \
                    or timestamp < self.first_value_timestamp:
                self.first_value_timestamp = timestamp

    def commit_events(self):
        store = DataStore()
        store.commit('events')

    def save(self, *args, **kwargs):
        result = super(Timeseries, self).save(*args, **kwargs)
        self.commit_events()
        return result


##class LogicalGroup(MP_Node):
##    """A group of time series.
##
##    End-users may group time series in any meaningful way. Furthermore, groups
##    can be combined into new groups. The resulting tree structure is modeled
##    via a materialized path approach.
##
##    """
##    name = models.CharField(max_length=64)
##    description = models.TextField()
##
##    class Meta:
##        app_label = APP_LABEL
