# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.txt
# -*- coding: utf-8 -*-
"""
To securely filter objects we don't have access to, we use a custom Django
object manager: ``TimeseriesManager``. We have to set that object manager
on our models.

"""
from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.db.models.query import GeoQuerySet
from django.db.models.manager import Manager
from tls import request
from treebeard.mp_tree import MP_NodeManager
from treebeard.mp_tree import MP_NodeQuerySet

from lizard_security.middleware import ALLOWED_DATA_SET_IDS


def user_data_set_ids():
    if request:
        user = getattr(request, 'user', None)
        if user is None or not user.is_superuser:
            return getattr(request, ALLOWED_DATA_SET_IDS, [])
    return None


class TimeseriesManager(Manager):
    """Manager that filters out ``Timeseries`` we have no permissions for."""

    def get_query_set(self):
        """Return base queryset, filtered by lizard-security's mechanism."""
        query_set = super(TimeseriesManager, self).get_query_set()
        data_set_ids = user_data_set_ids()
        if data_set_ids is None:
            return query_set
        return query_set.filter(data_set__in=data_set_ids)


class LocationQuerySet(GeoQuerySet, MP_NodeQuerySet):
    """Custom QuerySet that combines ``GeoQuerySet`` and ``MP_NodeQuerySet``.

    This tackles multiple inheritance problems: see ``LocationManager``.
    Note that while both super classes currently do have distinct
    methods, this might not be the case in the future.

    """

    def __init__(self, *args, **kwargs):
        super(LocationQuerySet, self).__init__(*args, **kwargs)


class LocationManager(GeoManager, MP_NodeManager):
    """Custom manager for the ``Location`` model class.

    We are bitten by multiple inheritance here: a ``GeoManager`` is required to
    support spatial queries, while an ``MP_NodeManager`` is needed by django-
    treebeard for manipulating trees. Both managers override get_query_set!
    This is solved by creating a custom ``LocationQuerySet``.

    """

    def get_query_set(self):
        # Satisfy both GeoManager and MP_NodeManager:
        query_set = LocationQuerySet(self.model,
            using=self._db).order_by('path')
        # Take permissions into account:
        data_sets = user_data_set_ids()
        if data_sets is None:
            return query_set
        return query_set.filter(timeseries__data_set__in=data_sets).distinct()
