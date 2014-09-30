# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import absolute_import
from __future__ import unicode_literals

from StringIO import StringIO
from datetime import datetime, timedelta
import logging
import os.path
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils import timezone
from django_extensions.db.fields import UUIDField

import magic
import networkx as nx
import pytz

from cassandralib.models import CassandraDataStore
from cassandralib.models import INTERNAL_TIMEZONE
from ddsc_core.models.treebeard_overrides import MP_Node_ByInstance
from lizard_security.models import DataOwner, DataSet

logger = logging.getLogger(__name__)

APP_LABEL = "ddsc_core"
CASSANDRA = getattr(settings, 'CASSANDRA', {})
FILENAME_FORMAT = '%Y-%m-%dT%H.%M.%S.%fZ'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls). __call__(*args, **kwargs)

        return cls._instances[cls]


class DataStore(CassandraDataStore):
    __metaclass__ = Singleton

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


class Location(BaseModel, MP_Node_ByInstance):
    """Location of a timeseries.

    Locations can be nested. The resulting tree is encoded via the materialized
    path algorithm and is best managed via the API provided by treebeard or
    the Django admin interface to keep it consistent.

    """
    #objects = manager.LocationManager()

    uuid = UUIDField(
        version=4,
        unique=True,
        help_text="universally unique identifier",
        verbose_name="UUID",
    )
    name = models.CharField(
        max_length=80,
        help_text="name of location",
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="optional description"
    )

    # The location described in words (exact location is unknown):
    relative_location = models.TextField(null=True, blank=True)
    # A single point that represents the real geometry (e.g. the center):
    point_geometry = models.PointField(srid=4258, null=True, blank=True)
    # The real geometry (point, linestring, polygon, etc):
    real_geometry = models.GeometryField(srid=4258, null=True, blank=True)
    # Precision in meters with respect to point_geometry:
    owner = models.ForeignKey(DataOwner, null=True, blank=True)
    geometry_precision = models.FloatField(
        null=True,
        blank=True,
        help_text="precision in meters with respect to point geometry"
    )
    created = models.DateTimeField(
        default=pytz.timezone('UTC').localize(datetime.utcnow()),
        help_text="datetime of creation in UTC"
    )
    show_on_map = models.BooleanField(
        default=True,
        help_text="whether to show the location on the map"
    )
    # Django's URLField is ment for absolute URLs (you cannot save a relative
    # URL via Django's Admin interface), so let's use a standard CharField.
    icon_url = models.CharField(
        max_length=200, blank=True, null=True,
        help_text="Absolute or relative URL to a non-standard icon used for "
        "displaying this location on the map. NB: relative URLs should be "
        "relative to the DDSC portal not the API website."
    )

    def __unicode__(self):
        return self.name

    def superlocation(self):
        try:
            return self.get_parent()
        except:
            pass

    def sublocations(self):
        try:
            return self.get_children()
        except:
            return []

    def get_srid(self):
        return 4258

    def save_under(self, parent_pk=None):
        '''
        Apparently Treebeard makes normal tree operations, like
        moving to a different parent node, really really hard...
        '''
        instance = self

        # Note that moving a node as `first-child` will trigger
        # a cascade update on all siblings and their childs,
        # with dramatic consequences for performance; so,
        # if the order is unimportant, append them as
        # `last-child`.

        if instance.pk is None:
            # creating a new instance
            if parent_pk is not None:
                # this is a new leaf node
                parent = instance.__class__.objects.get(pk=parent_pk)
                # We require treebeard 2.0 for its Django 1.5 support,
                # but apparently the API has changed a bit:
                ##instance = parent.add_child_by_instance(instance)
                instance = parent.add_child(instance=instance)
                instance.move(parent, pos='last-child')
            else:
                # this is a new tree root
                # We require treebeard 2.0 for its Django 1.5 support,
                # but apparently the API has changed a bit:
                ##instance = instance.__class__.add_root_by_instance(instance)
                instance = instance.__class__.add_root(instance=instance)
        else:
            # need to save first before we can operate on the parent
            instance.save()

            if parent_pk is not None:
                # node (and all children) have been moved somewhere in the tree
                parent = instance.__class__.objects.get(pk=parent_pk)
                instance.move(parent, pos='last-child')
            else:
                # node has become a new root node
                instance.move(
                    instance.__class__.get_first_root_node(),
                    pos='last-sibling'
                )

        # Reload the instance
        instance = instance.__class__.objects.get(pk=instance.pk)
        return instance


class LocationType(BaseModel):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=80, unique=True)
    locations = models.ManyToManyField(
        Location,
        blank=True,
        related_name="location_types"
    )

    def __unicode__(self):
        return self.name


class Timeseries(BaseModel):
    #objects = manager.TimeseriesManager()
    # The admin manager should be below the secured manager!!
    #objects_nosecurity = Manager()

    def __unicode__(self):
        return "{}".format(self.name)

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

    class ValidationFlag:
        NONE = '-1'
        OK = '0'
        DOUBTFUL = '3'
        UNRELIABLE = '6'

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

    uuid = UUIDField(
        version=4,
        unique=True,
        help_text="universally unique identifier",
        verbose_name="UUID",
    )
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="optional name for timeseries",
        db_index=True,
    )
    description = models.TextField(
        default="",
        blank=True,
        help_text="optional description for timeseries"
    )
    data_set = models.ManyToManyField(
        DataSet,
        related_name='timeseries',
        blank=True
    )

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

    validate_max_hard = models.FloatField(null=True, blank=True)
    validate_min_hard = models.FloatField(null=True, blank=True)
    validate_max_soft = models.FloatField(null=True, blank=True)
    validate_min_soft = models.FloatField(null=True, blank=True)
    validate_diff_hard = models.FloatField(null=True, blank=True)
    validate_diff_soft = models.FloatField(null=True, blank=True)
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
    created = models.DateTimeField(
        default=pytz.timezone('UTC').localize(datetime.utcnow()),
        help_text="datetime of creation in UTC"
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Timeseries"
        verbose_name_plural = "Timeseries"

    def get_value_type(self):
        value_type = dict(self.VALUE_TYPE)
        return value_type[self.value_type]

    def latest_value(self):
        if self.value_type in (Timeseries.ValueType.INTEGER,
                               Timeseries.ValueType.FLOAT):
            return self.latest_value_number
        if self.value_type == Timeseries.ValueType.TEXT:
            return self.latest_value_text
        return None

    def is_file(self):
        return self.value_type in (Timeseries.ValueType.IMAGE,
                                   Timeseries.ValueType.GEO_REMOTE_SENSING,
                                   Timeseries.ValueType.MOVIE,
                                   Timeseries.ValueType.FILE)

    def latest_value_file(self):
        if not self.is_file():
            raise Exception("Timeseries is not a file type.")
        if self.latest_value_timestamp:
            return self.latest_value_timestamp.strftime(FILENAME_FORMAT)
        return None

    def get_events(self, start=None, end=None, filter=None,
                   ignore_rejected=None):
        if filter is None:
            filter = ['value', 'flag']

        if start and (
            start.tzinfo is None
            or start.tzinfo.utcoffset(start) is None
        ):
            start = INTERNAL_TIMEZONE.localize(start)
        if end and (
            end.tzinfo is None
            or end.tzinfo.utcoffset(end) is None
        ):
            end = INTERNAL_TIMEZONE.localize(end)

        if (self.first_value_timestamp is None or
                self.latest_value_timestamp is None):
            # If there's no first or last timestamp, there's no data.
            # So make sure Cassandra returns nothing with no hard work.
            start = None
            end = None
        else:
            if start is None or start < self.first_value_timestamp:
                start = self.first_value_timestamp
            if end is None or end > self.latest_value_timestamp:
                end = self.latest_value_timestamp + timedelta(seconds=1)
            if start > end:
                start = None
                end = None

        store = DataStore()
        value_type_map = {
            Timeseries.ValueType.FLOAT: 'float',
            Timeseries.ValueType.INTEGER: 'integer',
        }
        convert_values_to = value_type_map.get(self.value_type)
        return store.read(
            'events', self.uuid, start, end, params=filter,
            convert_values_to=convert_values_to,
            ignore_rejected=ignore_rejected
        )

    def set_events(self, df):
        last = None
        for timestamp, row_obj in df.iterrows():
            row = row_obj.to_dict()

            # Validate.
            if 'value' in row and self.value_type in \
                    (Timeseries.ValueType.INTEGER, Timeseries.ValueType.FLOAT):

                value = float(row['value'])
                row['flag'] = Timeseries.ValidationFlag.NONE

                # When at least one boundary is set, the value can be 'OK'.
                if self.validate_max_soft is not None \
                        or self.validate_max_soft is not None \
                        or self.validate_min_hard is not None \
                        or self.validate_min_soft is not None \
                        or self.validate_diff_hard is not None \
                        or self.validate_diff_soft is not None:
                    row['flag'] = Timeseries.ValidationFlag.OK

                # Check soft boundaries, possibly marking value 'DOUBTFUL'.
                if self.validate_max_soft is not None \
                        and value > self.validate_max_soft:
                    row['flag'] = Timeseries.ValidationFlag.DOUBTFUL
                if self.validate_min_soft is not None \
                        and value < self.validate_min_soft:
                    row['flag'] = Timeseries.ValidationFlag.DOUBTFUL
                if self.validate_diff_soft is not None and last is not None \
                        and abs(last - value) > self.validate_diff_soft:
                    row['flag'] = Timeseries.ValidationFlag.DOUBTFUL

                # Check hard boundaries, possibly marking value 'UNRELIABLE'.
                if self.validate_max_hard is not None \
                        and value > self.validate_max_hard:
                    row['flag'] = Timeseries.ValidationFlag.UNRELIABLE
                if self.validate_min_hard is not None \
                        and value < self.validate_min_hard:
                    row['flag'] = Timeseries.ValidationFlag.UNRELIABLE
                if self.validate_diff_hard is not None and last is not None \
                        and abs(last - value) > self.validate_diff_hard:
                    row['flag'] = Timeseries.ValidationFlag.UNRELIABLE

                self.set_event(timestamp, row)
                last = value

    def set_event(self, timestamp, row):
        if timestamp.tzinfo is None or \
                timestamp.tzinfo.utcoffset(timestamp) is None:
            timestamp = INTERNAL_TIMEZONE.localize(timestamp)

        # Update first and latest value.
        if 'value' in row:
            if not self.latest_value_timestamp \
                    or self.latest_value_timestamp <= timestamp:
                if self.value_type in (
                    Timeseries.ValueType.INTEGER,
                    Timeseries.ValueType.FLOAT
                ):
                    self.latest_value_number = row['value']
                elif self.value_type in (
                        Timeseries.ValueType.TEXT,
                        Timeseries.ValueType.IMAGE,
                        Timeseries.ValueType.GEO_REMOTE_SENSING):
                    self.latest_value_text = row['value']
                self.latest_value_timestamp = timestamp
            if not self.first_value_timestamp \
                    or timestamp < self.first_value_timestamp:
                self.first_value_timestamp = timestamp

        store = DataStore()
        store.write_row('events', self.uuid, timestamp, row)

    def _data_dir(self, timestamp):
        paths = getattr(settings, 'IMPORTER_PATH')
        base_path = paths['storage_base_path']
        if self.value_type == Timeseries.ValueType.IMAGE:
            type_path = paths['image']
        elif self.value_type == Timeseries.ValueType.GEO_REMOTE_SENSING:
            type_path = paths['geotiff']
        elif self.value_type == Timeseries.ValueType.MOVIE:
            type_path = paths['video']
        elif self.value_type == Timeseries.ValueType.FILE:
            type_path = paths['file']
        else:
            type_path = paths['unrecognized']
        str_year = str(timestamp.year)
        str_month = str(timestamp.month)
        str_day = str(timestamp.day)
        date = str_year + '-' + str_month + '-' + str_day
        return '%s%s%s/%s/' % (base_path, type_path, self.uuid, date)

    def set_file(self, timestamp, content):
        if not self.is_file():
            raise Exception("Timeseries is not a file type.")
        if timestamp.tzinfo is None or \
                timestamp.tzinfo.utcoffset(timestamp) is None:
            timestamp = INTERNAL_TIMEZONE.localize(timestamp)
        dt = timestamp.strftime(FILENAME_FORMAT)
        data_dir = self._data_dir(timestamp)
        file_path = data_dir + dt
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(content)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        shutil.move(temp.name, file_path)
        row = {"datetime": dt, "value": file_path}
        self.set_event(timestamp, row)

    def get_file(self, timestamp):
        if not self.is_file():
            raise Exception("Timeseries is not a file type.")
        end = timestamp + timedelta(seconds=1)
        events = self.get_events(timestamp, end, ['value'])
        if (
            len(events) < 1
            or 'value' not in events
            or len(events['value']) < 1
        ):
            raise Exception("File not found.")
        file_path = events['value'][0]
        file_mime = magic.from_file(file_path, mime=True)
        io = StringIO(file(file_path, "rb").read())
        file_size = os.path.getsize(file_path)
        return (io.read(), file_mime, file_size)

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
    #objects = manager.LogicalGroupManager()

    name = models.CharField(max_length=64)
    owner = models.ForeignKey(DataOwner)
    description = models.TextField(blank=True)
    timeseries = models.ManyToManyField(Timeseries, blank=True,
                                        related_name="logical_groups")

    class Meta(BaseModel.Meta):
        ordering = ["owner", "name"]
        unique_together = ("owner", "name")

    def graph(self):
        return '<a href="{0}" target="_blank">graph</a>'.format(
            reverse('logical_group_graph', kwargs={'pk': self.pk})
        )

    # Do not escape HTML-output.
    graph.allow_tags = True

    def timeseries_count(self):
        """Return the number of timeseries in this group."""
        return self.timeseries.count()

    # Recursively grab all Timeseries in this Logical Group and its
    # descendants.
    def timeseries_r(self, max_depth=10):

        childs = self.get_child_ids()
        childs.append(self.id)

        return Timeseries.objects.filter(logical_groups__in=childs).distinct()

    def __unicode__(self):
        return self.name

    def get_child_ids(self):

        G = nx.DiGraph()
        G.add_edges_from([
            (obj.parent.id, obj.child.id)
            for obj in LogicalGroupEdge.objects.filter(
                parent__owner=self.owner).select_related('parent', 'child')
        ])
        if G.has_node(self.id):
            return G.successors(self.id)
        else:
            return []


class LogicalGroupEdge(BaseModel):
    """An edge between two nodes in the graph of LogicalGroups.

    Edges are directed: from child to parent. Cycles are not
    allowed. In other words, a directed acyclic graph (DAG).

    """
    child = models.ForeignKey(LogicalGroup, related_name="parents")
    parent = models.ForeignKey(LogicalGroup, related_name="childs")

    class Meta(BaseModel.Meta):
        unique_together = ("child", "parent")

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


class TimeseriesSelectionRule(BaseModel):
    """A simple, Django-like selection rule for timeseries.

    For example: source__manufacturer__code__exact='ALS'.

    Multiple rules can be chained together using the
    logical `AND` or `OR` operators.

    Generic relations are applied, because this model
    is used with both `LogicalGroup` and `DataSet`.

    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
        'content_type',
        'object_id'
    )
    operator = models.CharField(
        blank=True,
        choices=(('&', 'AND'), ('|', 'OR')),
        max_length=1,
        null=True,
    )
    criterion = models.CharField(max_length=128)

    class Meta(BaseModel.Meta):
        ordering = ["pk"]  # entry order

    def __unicode__(self):
        return self.criterion


class Manufacturer(BaseModel):
    """Manufacturer of a sensor."""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class Source(BaseModel):
    """A source of data, e.g. a sensor."""

    CALCULATED = 0
    SENSOR = 1
    SIMULATED = 2
    DERIVED = 3

    SOURCE_TYPES = (
        (CALCULATED, 'Calculated'),
        (SENSOR, 'Sensor'),
        (SIMULATED, 'Simulated'),
        (DERIVED, 'Derived'),
    )

    uuid = UUIDField(
        version=4,
        unique=True,
        help_text="universally unique identifier",
        verbose_name="UUID",
    )
    name = models.CharField(
        max_length=64,
        db_index=True,
    )
    source_type = models.SmallIntegerField(
        choices=SOURCE_TYPES,
        default=SENSOR,
    )
    owner = models.ForeignKey(DataOwner, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer)
    details = models.TextField(blank=True, null=True)
    created = models.DateTimeField(
        default=pytz.timezone('UTC').localize(datetime.utcnow()),
        help_text="datetime of creation in UTC"
    )
    frequency = models.IntegerField(
        blank=True,
        help_text="frequency at which data is obtained in seconds",
        null=True,
    )
    timeout = models.IntegerField(
        blank=True,
        help_text="timeout for triggering alarms in seconds",
        null=True,
    )

    def __unicode__(self):
        return "{}".format(self.name)


class TimeseriesGroup(BaseModel):
    """???

    Bastiaan (and only Bastiaan) knows.

    """
    name = models.CharField(max_length=64, unique=True)
    sources = models.ManyToManyField(Source)
    parameters = models.ManyToManyField('Parameter')


class SourceGroup(BaseModel):
    """???

    Bastiaan (and only Bastiaan) knows.

    """
    name = models.CharField(max_length=64, unique=True)
    sources = models.ManyToManyField(Source)
    description = models.TextField(blank=True)


class IdMapping(BaseModel):
    """Maps an internal timeseries ID on an external one."""
    timeseries = models.ForeignKey(Timeseries)
    user = models.ForeignKey(User)
    remote_id = models.CharField(max_length=64)


class StatusCache(BaseModel):
    """statistics for each timeseries among a certain time period"""

    #objects = manager.StatusCacheManager()
    # The admin manager should be below the secured manager!!
    #objects_nosecurity = Manager()

    timeseries = models.ForeignKey(Timeseries)
    nr_of_measurements_total = models.IntegerField(
        null=True, blank=True, db_index=True)
    nr_of_measurements_reliable = models.IntegerField(
        null=True, blank=True, db_index=True)
    nr_of_measurements_doubtful = models.IntegerField(
        null=True, blank=True, db_index=True)
    nr_of_measurements_unreliable = models.IntegerField(
        null=True, blank=True, db_index=True)
    min_val = models.FloatField(null=True, blank=True)
    max_val = models.FloatField(null=True, blank=True)
    mean_val = models.FloatField(null=True, blank=True)
    std_val = models.FloatField(null=True, blank=True)
    modify_timestamp = models.DateTimeField(null=True)
    date = models.DateField(null=True, db_index=True)

    def set_ts_status(self, df):
        self.nr_of_measurements_total = df['value'].count()
        histo = df['flag'].value_counts()
        try:
            self.nr_of_measurements_reliable = histo['0']
        except:
            self.nr_of_measurements_reliable = 0
        try:
            self.nr_of_measurements_doubtful = histo['3']
        except:
            self.nr_of_measurements_doubtful = 0
        try:
            self.nr_of_measurements_unreliable = histo['6']
        except:
            self.nr_of_measurements_unreliable = 0
        self.modify_timestamp = timezone.now()
        self.mean_val = df['value'].mean(0)
        self.max_val = df['value'].max(0)
        self.min_val = df['value'].min(0)
        self.std_val = df['value'].std(0)
        self.save()
