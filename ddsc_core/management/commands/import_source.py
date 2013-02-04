#from adaptor.model import CsvDbModel
from django.core.management.base import BaseCommand
from ddsc_core.models.models import Source
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

        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0 :
                    uuid = row[1]
                    name = row[2]
                    manufacture = row[3]
                    source_type = row[4]
                    details = row[5]
                    
                    Source.objects.create(name=name, 
                                          source_type=1, ## hard code because currently TYPE and source_type are 2 different stories
                                          manufacturer_id = 1,  ## for now, dummy since no data
                                          details = details,
                                          uuid = uuid)
                    
                    
                    
