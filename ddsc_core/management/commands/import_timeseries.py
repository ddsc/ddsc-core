#from adaptor.model import CsvDbModel
from django.core.management.base import BaseCommand
from ddsc_core.models.models import Timeseries, Source
from ddsc_core.models.aquo import Unit, Parameter, Compartment, MeasuringDevice, MeasuringMethod
from ddsc_core.models.aquo import ReferenceFrame, ProcessingMethod
import string
#from ddsc_core.models import Location
import csv


class Command(BaseCommand):
    args = '<CSV/sql file>'
    help = 'Imports a CSV file of timeseries into the database.'

    def handle(self, *args, **options):

        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0 :
                    uuid = row[0]
                    name = row[1]
                    description = row[2]
                    
                    type = string.lower(row[3])
                    def f(x):
                        return {
                            'integer': 0,
                            'float': 1,
                            'text': 4,
                            'image': 5,
                            'geo_remote_sensing': 7,
                            'movie': 8,
                            'file': 10,
                        }.get(x, 1)
                    value_type = f(type)
                    
                    try: 
                        lc = Location.objects.get(uuid=row[8])
                        location_id = lc.id
                    except:
                        location_id = 1 # not matching
                    
                    try: 
                        pr = Parameter.objects.get(code=row[9])
                        parameter_id = pr.id
                    except:
                        parameter_id = 1 # not matching
                        
                    try: 
                        ut = Unit.objects.get(code=row[10])
                        unit_id = ut.id
                    except:
                        unit_id = 1 # not matching
                        
                    try: 
                        rf = ReferenceFrame.objects.get(code=row[11])
                        reference_f_id = rf.id
                    except:
                        reference_f_id = 1 # not matching
                        
                    try: 
                        cp = Compartment.objects.get(code=row[12])
                        compartment_id = cp.id
                    except:
                        compartment_id = 1 # not matching
                        
                    try: 
                        md = MeasuringDevice.objects.get(code=row[13])
                        measuring_device_id = md.id
                    except:
                        measuring_device_id = 1 # not matching
                        
                    try: 
                        mm = MeasuringMethod.objects.get(code=row[14])
                        measuring_method_id = mm.id
                    except:
                        measuring_method_id = 1 # not matching
                    
                    try: 
                        pm = ProcessingMethod.objects.get(code=row[15])
                        processing_method_id = pm.id
                    except:
                        processing_method_id = 1 # not matching
                        
                    try: 
                        src = Source.objects.get(uuid=row[7])
                        source_id = src.id
                    except:
                        source_id = 31 # not matching
                        
                        
                    
                    Timeseries.objects.create(name=name, description=description, value_type=value_type,
                                              location_id=location_id, parameter_id=parameter_id,
                                              unit_id=unit_id, reference_frame_id = reference_f_id,
                                              compartment_id=compartment_id, measuring_device_id=measuring_device_id,
                                              measuring_method_id=measuring_method_id, 
                                              processing_method_id=processing_method_id, source_id=source_id)
                    
        print "completeted~!"
