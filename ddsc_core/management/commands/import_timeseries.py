# (c) Fugro GeoServices. MIT licensed, see LICENSE.rst.
import string
import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from ddsc_core.models.models import Timeseries, Source, Location, IdMapping
from ddsc_core.models.aquo import Unit, Parameter, Compartment
from ddsc_core.models.aquo import MeasuringDevice, MeasuringMethod
from ddsc_core.models.aquo import ReferenceFrame, ProcessingMethod
from lizard_security.models import DataOwner


class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of timeseries into the database.'

    def handle(self, *args, **options):
        dataowner = args[1]
        do, created = DataOwner.objects.get_or_create(name=dataowner)
        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0:
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
                        lc = Location.objects.get(uuid=row[7])
                    except:
                        lc = Location.objects.get(name='unknown')
                    location_id = lc.id
                    try:
                        pr = Parameter.objects.get(code=row[8].split('-')[0])
                    except:
                        pr = Parameter.objects.get(code='unknown')
                    parameter_id = pr.id
                    try:
                        ut = Unit.objects.get(code=row[9])
                    except:
                        try:
                            ut = Unit.objects.get(description=row[9])
                        except:
                            ut = Unit.objects.get(code='unknown')
                    unit_id = ut.id
                    try:
                        rf = ReferenceFrame.objects.get(
                            code=row[10].split('-')[0])
                    except:
                        rf = ReferenceFrame.objects.get(code='unknown')
                    reference_f_id = rf.id
                    try:
                        cp = Compartment.objects.get(
                            code=row[11].split('-')[0])
                    except:
                        cp = Compartment.objects.get(code='unknown')
                    compartment_id = cp.id
                    try:
                        md = MeasuringDevice.objects.get(
                            code=row[12].split('-')[0])
                    except:
                        md = MeasuringDevice.objects.get(code='unknown')
                    measuring_device_id = md.id
                    try:
                        mm = MeasuringMethod.objects.get(
                            code=row[13].split('-')[0])
                    except:
                        mm = MeasuringMethod.objects.get(code='unknown')
                    measuring_method_id = mm.id
                    try:
                        pm = ProcessingMethod.objects.get(
                            code=row[14].split('-')[0])
                    except:
                        pm = ProcessingMethod.objects.get(code='unknown')
                    processing_method_id = pm.id
                    try:
                        src = Source.objects.get(uuid=row[6])
                    except:
                        src = Source.objects.get(uuid='unknown')
                    source_id = src.id
                    Timeseries.objects.create(name=name,
                        description=description, value_type=value_type,
                        location_id=location_id, parameter_id=parameter_id,
                        unit_id=unit_id, reference_frame_id=reference_f_id,
                        compartment_id=compartment_id,
                        measuring_device_id=measuring_device_id,
                        measuring_method_id=measuring_method_id, uuid=uuid,
                        processing_method_id=processing_method_id,
                        source_id=source_id)
                    usr = row[4]
                    remote_id = row[5]
                    ts = Timeseries.objects.get(uuid=uuid)
                    user = User.objects.get(username=usr)
                    IdMapping.objects.create(
                        user_id=user.pk,
                        remote_id=remote_id,
                        timeseries_id=ts.pk)
                    ts.owner_id = do.pk
                    ts.save()

        print "completeted~!"
