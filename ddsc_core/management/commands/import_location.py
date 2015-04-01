# (c) Fugro GeoServices, Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple
from datetime import datetime
import csv

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
import pytz

from ddsc_core.models import Location
from ddsc_core.utils import transform

ETRS89 = 4258  # European Terrestrial Reference System 1989

# The named fields below correspond to the 12 columns in Fugro's Excel sheet.
# Fugro did not process `real_geometry` and `srid_real_geometry` in their
# original code. Question: why would one need `srid_real_geometry` if
# `real_geometry` is in EWKT?

row = namedtuple(
    'LocationRow', 'uuid, name, x, y, z, srid, parent_uuid, real_geometry, '
    'srid_real_geometry, description, geometry_precision, relative_location'
)

# Apparently, `real_geometry` has not been missed in 2 years, so it may
# safely be regarded as obsolete.


class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of locations into the database.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        with open(args[0], 'rU') as f:

            # Loop over each row (i.e. Location) in the CSV file.
            for r in map(row._make, csv.reader(f)):

                # Create a new instance of Location.
                if r.parent_uuid:
                    # It's a child node.
                    parent = Location.objects.get(uuid=r.parent_uuid)
                    location = parent.add_child(name=r.name)
                else:
                    # It's a root node.
                    location = Location.add_root(name=r.name)

                # Assign properties.
                location.description = r.description
                location.geometry_precision = str2float(r.geometry_precision)
                point_geometry = point(r)
                location.point_geometry = point_geometry
                location.show_on_map = True if point_geometry else False
                location.relative_location = r.relative_location
                location.uuid = r.uuid
                location.created = datetime.now(tz=pytz.utc)

                # Persist to database.
                self.stdout.write("Saving {}.".format(location))
                location.save()


def str2float(s):
    "Create a float from its string representation."
    try:
        f = float(s)
    except ValueError:
        f = None
    return f


def point(r):
    "Create an ETRS89 point from x, y, z and srid."
    try:
        p = Point([float(r.x), float(r.y), float(r.z)], srid=int(r.srid))
        p = transform(p, ETRS89, clone=True)
    except ValueError:
        p = None
    return p
