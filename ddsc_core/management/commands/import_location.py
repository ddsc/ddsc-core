#from adaptor.model import CsvDbModel
from django.core.management.base import BaseCommand
from ddsc_core.models.models import Location
#from ddsc_core.models import Location
import csv

from django.contrib.gis.geos import GEOSGeometry

#class MyCsvModel(CsvDbModel):
#
#    class Meta:
#        dbModel = Location
#        delimiter = ","

class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of locations into the database.'

    def handle(self, *args, **options):
        self.stdout.write('Foobar "%s"' % args[0])
        i = 1
        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0 :
                    uuid = row[0]
                    name = row[1]
                    x = row[3]
                    y = row[4]
                    z = row[5]
                    srid = row[6]
                    parentuuid = row[7]
                    description = row[10]
                    if row[11] is not '':
                        geometry_precision = row[11]
                    else:
                        geometry_precision = None
                    location_description = row[12]
                    location_type = row[13]
                    
                    if x is not '':
                        geo_input = 'POINT(' + x +' ' + y + ' ' + z +')'
                        print geo_input
                        point_geometry = GEOSGeometry(geo_input, srid)
                    else :
                        point_geometry = ''
                        
                    path = i 
                    i+=1
                    Location.objects.create(name=name, 
                                            description=description,
                                            geometry_precision=geometry_precision,
                                            point_geometry=point_geometry,
                                            real_geometry='',
                                            depth=1,
                                            numchild=0,
                                            path = i,
                                            relative_location=location_description,
                                            uuid=uuid)
                    
                    
                    
