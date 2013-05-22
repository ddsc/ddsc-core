# (c) Fugro GeoServices. MIT licensed, see LICENSE.rst.
from django.core.management.base import BaseCommand
from ddsc_core.models.models import Location

import csv
from django.utils import timezone

from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of locations into the database.'

    def handle(self, *args, **options):
        loc_latest = Location.objects.latest("pk")
        root_nodes = loc_latest.__class__.get_root_nodes()
        i = len(root_nodes) + 5
        count = 0
        maintain_list = []
        nr_0 = 0
        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0:
                    uuid = row[0]
                    name = row[1]
                    x = row[2]
                    y = row[3]
                    z = row[4]
                    srid = row[5]
                    parentuuid = row[6]
                    if len(parentuuid) < 5:
                        maintain_list.append(0)
                        nr_0 += 1
                    else:
                        maintain_list.append(parentuuid)
                    description = row[9]
                    if row[10] is not '':
                        geometry_precision = row[10]
                    else:
                        geometry_precision = None
                    location_description = row[11]
                    if x is not '':
                        geo_input = 'POINT(' + x + ' ' + y + ' ' + z + ')'
                        point_geometry = GEOSGeometry(geo_input, int(srid))
                    else:
                        point_geometry = ''
                    Location.objects.create(name=name,
                        description=description,
                        geometry_precision=geometry_precision,
                        point_geometry=point_geometry,
                        real_geometry='',
                        depth=1,
                        numchild=0,
                        path='{0:04}'.format(i),
                        relative_location=location_description,
                        uuid=uuid, created=timezone.now())
                    i += 1
                    count += 1
            loc_latest = Location.objects.latest("pk")
            j = loc_latest.pk - count + 1
            print 'first loop completed!'
            print 'nr. of root nodes are: ' + str(nr_0)
#            while sum(maintain_list) is not 0 :
            print j
            for st in maintain_list:
                if st != 0:
                    currentnode = Location.objects.get(pk=j)
                    try:
                        parentnode = Location.objects.get(uuid=st)
                        currentnode.save_under(parentnode.pk)
                    except:
                        currentnode = currentnode.save_under()

                j += 1
        print "all completeted~!"
