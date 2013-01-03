# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.txt
# -*- coding: utf-8 -*-
"""
To securely filter our objects we don't have access to, we use a custom Django
object manager: ``FilteredManager``. We have to set that object manager on our
models.

"""
from django.contrib.gis.db.models import GeoManager
from django.db.models.manager import Manager
from tls import request
from treebeard.mp_tree import MP_NodeManager

from lizard_security.middleware import ALLOWED_DATA_SET_IDS


def user_data_set_ids():
    user = None
    if request:
        user = getattr(request, 'user', None)
        if user is None or not user.is_superuser:
            return getattr(request, ALLOWED_DATA_SET_IDS, [])
    return None


class TimeseriesManager(Manager):
    """Custom manager that filters out objects whose data set we can't access.
    """
    def get_query_set(self):
        """Return base queryset, filtered through lizard-security's mechanism.
        """
        query_set = super(TimeseriesManager, self).get_query_set()
        data_set_ids = user_data_set_ids()
        if data_set_ids is None:
            return query_set
        return query_set.filter(data_set__in=data_set_ids)


class LocationManager(MP_NodeManager, GeoManager):
    """Custom geomanager that filters out objects whose data set we can't
    access.
    """
    def get_query_set(self):
        """Return base queryset, filtered through lizard-security's mechanism.
        """
        query_set = super(LocationManager, self).get_query_set()
        data_sets = user_data_set_ids()
        if data_sets is None:
            return query_set
        return query_set.filter(timeseries__data_set__in=data_sets).distinct()
