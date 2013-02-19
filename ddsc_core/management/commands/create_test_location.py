from django.core.management.base import BaseCommand
from ddsc_core.models import (
    Location,
    Source,
    Parameter,
    Unit,
    Timeseries
)
from lizard_security.models import DataSet
from django.contrib.gis.geos import Point
import pandas as pd
import numpy as np
import datetime
import pytz

TEST_LOCATION_NAME = 'Test Location'
TEST_TIMESERIES_NAME = 'Test Timeseries'
TEST_PARAMETER_NAME = 'Test Param'
TEST_UNIT_NAME = 'Test Unit'

class Command(BaseCommand):
    args = '[nothing]'
    help = 'Create a test location and timeseries in the database.'

    def handle(self, *args, **options):
        data_sets = DataSet.objects.all()
        data_set = data_sets[0] if len(data_sets) > 0 else None
        
        sources = Source.objects.all()
        source = sources[0] if len(sources) > 0 else None

        parameters = Parameter.objects.filter(code=TEST_PARAMETER_NAME)
        parameter = parameters[0] if len(parameters) > 0 else None

        if not parameter:
            parameter = Parameter(
                code=TEST_PARAMETER_NAME,
                group='{} group'.format(TEST_PARAMETER_NAME),
                begin_date=datetime.datetime.now(),
                end_date=datetime.datetime.now(),
            )
            parameter.save()

        units = Unit.objects.filter(code=TEST_UNIT_NAME)
        unit = units[0] if len(units) > 0 else None

        if not unit:
            unit = Unit(
                code=TEST_UNIT_NAME,
                begin_date=datetime.datetime.now(),
                end_date=datetime.datetime.now(),
            )
            unit.save()

        locations = Location.objects.filter(name=TEST_LOCATION_NAME)
        location = locations[0] if len(locations) > 0 else None

        if not location:
            location = Location(
                name=TEST_LOCATION_NAME,
                description='{} description'.format(TEST_LOCATION_NAME),
                point_geometry=Point(0, 0),
            )
            location.save_under(None)

        timeseriess = Timeseries.objects.filter(name=TEST_TIMESERIES_NAME)
        timeseries = timeseriess[0] if len(timeseriess) > 0 else None

        if not timeseries:
            timeseries = Timeseries(
                name=TEST_TIMESERIES_NAME,
                description='{} description'.format(TEST_TIMESERIES_NAME),
                source=source,
                parameter=parameter,
                unit=unit,
                locations=location
            )
            timeseries.save()
            timeseries.data_sets = [data_set]
            timeseries.save()

        events = timeseries.get_events()
        if len(events) == 0:
            dates = pd.date_range('1/1/2011', periods=20000, freq='1Min', tz=pytz.UTC)
            vals = np.linspace(-np.pi, np.pi, len(dates))
            vals = np.sin(vals)
            df = pd.DataFrame(vals, index=dates, columns=['value'])
            timeseries.set_events(df)

        timeseries.save()
