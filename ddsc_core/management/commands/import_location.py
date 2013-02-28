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
        i = Location.objects.count() + 1
        second_loop_start = i
        maintain_list=[]
        nr_0 = 0
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
                    
                    if parentuuid == 'N/A':
                        maintain_list.append(0)
                        nr_0 += 1
                    else :
                        maintain_list.append(parentuuid)
                    
                    description = row[10]
                    
                    if row[11] is not '':
                        geometry_precision = row[11]
                    else:
                        geometry_precision = None
                        
                    location_description = row[12]
                    location_type = row[13]
                    
                    if x is not '':
                        geo_input = 'POINT(' + x +' ' + y + ' ' + z +')'
                        point_geometry = GEOSGeometry(geo_input, srid)
                    else :
                        point_geometry = ''
                        
                    path = i 
                    
                    Location.objects.create(id=i,
                                            name=name, 
                                            description=description,
                                            geometry_precision=geometry_precision,
                                            point_geometry=point_geometry,
                                            real_geometry='',
                                            depth=1,
                                            numchild=0,
                                            path = '{0:04}'.format(i),
                                            relative_location=location_description,
                                            uuid=uuid)
                    i+=1
                    
            print 'first loop completed!'
            print 'nr. of root nodes are: ' + str(nr_0)
            
            i = second_loop_start
#            while sum(maintain_list) is not 0 :
            print i 
            for st in maintain_list:
                if st != 0 :
                    #print st  # for debuging
                    currentnode = Location.objects.get(id=i)
#                    print currentnode
                    try :
                        parentnode = Location.objects.get(uuid=st)
#                        print parentnode
                        currentnode.save_under(parentnode.pk)
                    except :
                        currentnode.path = 'N/A' + str(i)
                        currentnode.depth = 9999
                        currentnode.numchild = 9999
                        currentnode.save()
                i += 1
                                
                    
        print "all completeted~!"
                    
