# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models.manager import Manager
from treebeard.mp_tree import MP_Node
import networkx as nx

from cassandralib.models import CassandraDataStore
from cassandralib.models import INTERNAL_TIMEZONE
from ddsc_core import manager
from lizard_security.models import DataOwner, DataSet

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
    """Super class of ddsc_core models.

    Instead of having a single models.py, ddsc_core models have been split
    over multiple modules. This approach, however, has some issues with
    South, which have been solved by explicitly setting the app_label.

    """
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
        help_text="optional description for timeseries"
    )

    #relative_location
    point_geometry = models.PointField(srid=4326, null=True, blank=True)
    real_geometry = models.GeometryField(srid=4326, null=True, blank=True)
    geometry_precision = models.FloatField(
        null=True,
        blank=True,
        help_text="precision in meters of location"
    )

    def __unicode__(self):
        return self.name


class LocationType(BaseModel):
    name = models.CharField(max_length=80)
    locations = models.ManyToManyField(
        Location,
        blank=True,
        related_name="location_types"
    )

    def __unicode__(self):
        return self.name


class Timeseries(BaseModel):
    objects_nosecurity = Manager()
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

    # TODO: TimeseriesType is not used at the moment.
    # Delete it or add a timeseries_type attribute?
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
        help_text="optional name for timeseries"
    )
    description = models.TextField(
        default="",
        blank=True,
        help_text="optional description for timeseries"
    )
    data_set = models.ManyToManyField(DataSet, related_name='timeseries')

    supplying_systems = models.ManyToManyField(
        User,
        blank=True,
        through='IdMapping',
    )

    #type information
    value_type = models.SmallIntegerField(default=1, choices=VALUE_TYPE)

    source = models.ForeignKey('Source', null=True, blank=True)
    owner = models.ForeignKey(DataOwner, null=True, blank=True)
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        related_name='timeseries'
    )

    # References to Aquo Domain Tables
    parameter = models.ForeignKey('Parameter')
    unit = models.ForeignKey('Unit')
    reference_frame = models.ForeignKey(
        'ReferenceFrame',
        null=True,
        blank=True
    )
    compartment = models.ForeignKey('Compartment', null=True, blank=True)
    measuring_device = models.ForeignKey(
        'MeasuringDevice',
        null=True,
        blank=True
    )
    measuring_method = models.ForeignKey(
        'MeasuringMethod',
        null=True,
        blank=True
    )
    processing_method = models.ForeignKey(
        'ProcessingMethod',
        null=True,
        blank=True
    )

    validate_max_hard = models.FloatField(default=9999)
    validate_min_hard = models.FloatField(default=9999)
    validate_max_soft = models.FloatField(default=9999)
    validate_min_soft = models.FloatField(default=9999)
    validate_max_diff = models.FloatField(default=9999)
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
        if self.value_type in (Timeseries.ValueType.INTEGER,
                Timeseries.ValueType.FLOAT):
            return self.latest_value_number
        if self.value_type in (Timeseries.ValueType.TEXT,
                Timeseries.ValueType.IMAGE):
            return self.latest_value_text

    def get_events(self, start=None, end=None, filter=None):
        if end is None:
            end = datetime.now()
        if start is None:
            start = end + relativedelta(years=-5)
        if filter is None:
            filter = ['value', 'flag']

        start = INTERNAL_TIMEZONE.localize(start)
        end = INTERNAL_TIMEZONE.localize(end)

        if (self.first_value_timestamp is None or
                self.latest_value_timestamp is None):
            # If there's no first or last timestamp, there's no data.
            # So make sure Cassandra returns nothing with no hard work.
            start = INTERNAL_TIMEZONE.localize(datetime.now())
            end = start + relativedelta(years=-10)
        else:
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


class LogicalGroup(BaseModel):
    """A group of time series.

    End-users may group time series in any meaningful way. Furthermore,
    groups can be combined into new groups.

    """
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(DataOwner)
    description = models.TextField(blank=True)
    timeseries = models.ManyToManyField(Timeseries, blank=True)

    def graph(self):
        return '<img src="{0}"/>'.format(
            reverse('logical_group_graph', kwargs={'pk': self.pk})
        )

    # Do not escape HTML-output.
    graph.allow_tags = True

    def __unicode__(self):
        return self.name

    class Meta(BaseModel.Meta):
        ordering = ["owner", "name"]
        unique_together = ("owner", "name")


class LogicalGroupEdge(BaseModel):
    """An edge between two nodes in the graph of LogicalGroups.

    Edges are directed: from child to parent. Cycles are not
    allowed. In other words, a directed acyclic graph (DAG).

    """
    child = models.ForeignKey(LogicalGroup, related_name="childs")
    parent = models.ForeignKey(LogicalGroup, related_name="parents")

    @classmethod
    def edges(cls):
        """Return a list of edge-tuples."""
        return [(obj.child, obj.parent) for obj in cls.objects.all()]

    @transaction.commit_on_success
    def save(self, *args, **kwargs):
        """Create an edge between 2 logical groups.

        Rollback if:

        1) the groups have different owners.
        2) the graph is not a DAG.

        """
        if self.child.owner != self.parent.owner:
            raise Exception("Nodes have different owners.")
        super(LogicalGroupEdge, self).save(*args, **kwargs)
        G = nx.DiGraph()
        G.add_edges_from(self.edges())
        if not nx.is_directed_acyclic_graph(G):
            raise Exception("Not a directed acyclic graph.")

    def __unicode__(self):
        return "{0} -> {1}".format(self.child, self.parent)

    class Meta(BaseModel.Meta):
        unique_together = ("child", "parent")


class Manufacturer(BaseModel):
    """Manufacturer of a sensor."""
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return '{}'.format(self.name)

class Source(BaseModel):
    """A source of data, e.g. a sensor."""

    CALCULATED = 0
    SENSOR = 1
    SIMULATED = 2

    SOURCE_TYPES = (
        (CALCULATED, 'Calculated'),
        (SENSOR, 'Sensor'),
        (SIMULATED, 'Simulated'),
    )

    name = models.CharField(max_length=64)
    source_type = models.SmallIntegerField(
        choices=SOURCE_TYPES,
        default=SENSOR,
    )
    manufacturer = models.ForeignKey(Manufacturer)
    details = models.TextField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        unique_together = ("manufacturer", "name")


class TimeseriesGroup(BaseModel):
    """???

    Bastiaan (and only Bastiaan) knows.

    """
    name = models.CharField(max_length=64)
    sources = models.ManyToManyField(Source)
    parameters = models.ManyToManyField('Parameter')


class SourceGroup(BaseModel):
    """???

    Bastiaan (and only Bastiaan) knows.

    """
    name = models.CharField(max_length=64)
    sources = models.ManyToManyField(Source)
    description = models.TextField(blank=True)


class IdMapping(BaseModel):
    """Maps an internal timeseries ID on an external one."""
    timeseries = models.ForeignKey(Timeseries)
    user = models.ForeignKey(User)
    remote_id = models.CharField(max_length=64)
