# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from datetime import datetime
from django.test import TestCase
from ddsc_core.models import DataStore, Location, Timeseries

import pandas as pd
import pytz


COLNAME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
INTERNAL_TIMEZONE = pytz.UTC


class DataStoreTest(TestCase):

    def test_setup(self):
        store = DataStore()
        store.truncate("events")

    def test_datastore_singleton(self):
        store1 = DataStore()
        store2 = DataStore()
        self.assertEquals(store1, store2, "DataStore should be singleton")


class LocationTest(TestCase):

    def test_location(self):
        code = 'LOCATION_37'
        with self.assertRaises(Location.DoesNotExist):
            loc0 = Location.objects.get(code=code)
        loc1 = Location.objects.create(code=code)
        loc1.save()
        loc2 = Location.objects.get(code=code)
        self.assertEquals(code, loc2.code, "Location should persist")


class TimeseriesTest(TestCase):
    
    def test_timeseries(self):
        code = 'TIMESERIES_37'
        with self.assertRaises(Timeseries.DoesNotExist):
            series0 = Timeseries.objects.get(code=code)
        series1 = Timeseries.objects.create(code=code)
        series1.save()
        series2 = Timeseries.objects.get(code=code)
        self.assertEquals(code, series2.code, "Timeseries should persist")

    def test_timeseries_event(self):
        code = 'TIMESERIES_37'
        date1 = datetime.strptime('2009-03-26T00:00:00Z', COLNAME_FORMAT)
        date1 = INTERNAL_TIMEZONE.localize(date1)
        values1 = {'value' : 42, 'flag' : 2}
        series1 = Timeseries.objects.create(code=code)
        series1.set_event(date1, values1)
        series1.save()
        series2 = Timeseries.objects.get(code=code)
        start = datetime.strptime('2009-03-26T00:00:00Z', COLNAME_FORMAT)
        end = datetime.strptime('2009-03-28T00:00:00Z', COLNAME_FORMAT)
        df2 = series2.get_events(start, end)
        self.assertEquals(1, len(df2))
        self.assertEquals('42', df2.get_value(date1, 'value'))
        self.assertEquals('2', df2.get_value(date1, 'flag'))

    def test_timeseries_events(self):
        code = 'TIMESERIES_37'
        date1 = datetime.strptime('2009-03-26T00:00:00Z', COLNAME_FORMAT)
        date1 = INTERNAL_TIMEZONE.localize(date1)
        date2 = datetime.strptime('2009-03-27T00:00:00Z', COLNAME_FORMAT)
        date2 = INTERNAL_TIMEZONE.localize(date2)
        datetimes = [date1, date2]
        data = {'value' : [43, 44], 'flag' : [3, 4]}
        series1 = Timeseries.objects.create(code=code)
        df1 = pd.DataFrame(data=data, index=datetimes)
        series1.set_events(df1)
        series1.save()
        series2 = Timeseries.objects.get(code=code)
        start = datetime.strptime('2009-03-26T00:00:00Z', COLNAME_FORMAT)
        end = datetime.strptime('2009-03-28T00:00:00Z', COLNAME_FORMAT)
        df2 = series2.get_events(start, end)
        self.assertEquals(2, len(df2))
        self.assertEquals('43', df2.get_value(date1, 'value'))
        self.assertEquals('3', df2.get_value(date1, 'flag'))
        self.assertEquals('44', df2.get_value(date2, 'value'))
        self.assertEquals('4', df2.get_value(date2, 'flag'))
