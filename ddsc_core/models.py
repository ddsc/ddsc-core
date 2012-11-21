# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from cassandralib.models import CassandraDataStore
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.gis.db import models
from lizard_security.models import UserGroup

import jsonfield
import pandas as pd
import pytz
import uuid


CASSANDRA = getattr(settings, 'CASSANDRA', {})
COLNAME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
INTERNAL_TIMEZONE = pytz.UTC


class DataStore(CassandraDataStore):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Location(models.Model):
    """
    Location
    Location of timeseries

    """
    code = models.CharField(
        primary_key=True,
        max_length=12,
        help_text="code for identification of location"
    )
    name = models.CharField(
        max_length=80,
        help_text="name of location"
    )
    description = models.TextField(
        default="",
        help_text='optional description for timeseries'
    )

    #relative_location
    point_geometry = models.PointField(dim=3, null=True)
    real_geometry = models.GeometryField(dim=3, null=True)
    geometry_precision = models.FloatField(
        null=True,
        help_text='precision in meters of location'
    )


class Timeseries(models.Model):
    INTEGER = 0
    FLOAT = 1
    TEXT = 4
    IMAGE = 5
    GEO_REMOTE_SENSING = 7
    MOVIE = 8
    FILE = 10

    VALUE_TYPE = (
        (INTEGER, 'integer'),
        (FLOAT, 'float'),
        (TEXT, 'text'),
        (IMAGE, 'image'),
        (GEO_REMOTE_SENSING, 'georeferenced remote sensing'),
        (MOVIE, 'movie'),
        (FILE, 'file'),
    )

    HISTORICAL = 0
    SIMULATED_FORECAST = 1
    SIMULATED_HISTORICAL = 2

    TIMESERIES_TYPE = (
        (HISTORICAL, 'historical'),
        (SIMULATED_FORECAST, 'simulated forecast'),
        (SIMULATED_HISTORICAL, 'simulated historical'),
    )

    code = models.CharField(
        primary_key=True,
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
        help_text='optional description for timeseries'
    )

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
        related_name='timeseries'
    )

    #observationType = models.ForeignKey(ObservationType)
    #instrument_type = models.ForeignKey(InstrumentType, null=True)
    #valuation_method = models.ForeignKey(ValuationMethod, null=True)
    #process_method = models.ForeignKey(ProcessMethod, null=True)

    def get_series_data(self):

        try:
            start = datetime.now() + relativedelta(years=-3)
            end = datetime.now()
            filter = ['value', 'flag']

            store = DataStore(
                CASSANDRA['servers'],
                CASSANDRA['keyspace'],
                CASSANDRA['column_family'],
                10000
            )
            df = store.read(
                self.code,
                INTERNAL_TIMEZONE.localize(start),
                INTERNAL_TIMEZONE.localize(end),
                params=filter
            )

            data = [
                dict([('datetime', timestamp.strftime(COLNAME_FORMAT))] + [
                    (colname, row[i])
                    for i, colname in enumerate(df.columns)
                ])
                for timestamp, row in df.iterrows()
            ]
            return data

        except Exception as ex:
            print repr(ex)
            return []
