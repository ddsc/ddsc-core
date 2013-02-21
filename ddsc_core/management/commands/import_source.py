#from adaptor.model import CsvDbModel
from django.core.management.base import BaseCommand
from ddsc_core.models.models import Source, Manufacturer
#from ddsc_core.models import Location
import csv
import string

from django.contrib.gis.geos import GEOSGeometry

#class MyCsvModel(CsvDbModel):
#
#    class Meta:
#        dbModel = Location
#        delimiter = ","

class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of source into the database.'

    def handle(self, *args, **options):

        i = 1
        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0 :
                    uuid = row[1]
                    name = row[2]
                    manufacturer = row[3]
                    print manufacturer  # for testing
                    try: 
                        manufacturer = Manufacturer.objects.get(name=manufacturer)
                        manufacturer_id = manufacturer.id
                        print manufacturer_id  # for testing
                        type = string.lower(row[4])
                        def f(x):
                            return {
                                'calculated': 0,
                                'sensor': 1,
                                'simulated': 2,
                                'derived': 3,
                            }.get(x, 1)
                        source_type = f(type)
                        details = row[5]                        
                        Source.objects.create(name=name, id=str(i), 
                                              source_type=source_type, ## hard code because currently TYPE and source_type are 2 different stories
                                              manufacturer_id = manufacturer_id,  ## for now, dummy since no data
                                              details = details,
                                              uuid = uuid)
                        i+=1
                        
                    except :
                        print 'can not find Manufacure info for row : %r' % str(i)
                        i+=1      
                
                    
        print "completeted~!"
                    
                    
                    
