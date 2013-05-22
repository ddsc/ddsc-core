# (c) Fugro GeoServices. MIT licensed, see LICENSE.rst.
from django.core.management.base import BaseCommand
from ddsc_core.models.models import Source, Manufacturer

from django.utils import timezone
import csv
import string


class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of source into the database.'

    def handle(self, *args, **options):
        with open(args[0], 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 0:
                    uuid = row[0]
                    name = row[1]
                    manufacturer = row[2]
                    print manufacturer  # for testing
                    try:
                        manufacturer = Manufacturer.objects.get(
                            name=manufacturer)
                        manufacturer_id = manufacturer.id
                    except:
                        manufacturer = Manufacturer.objects.get(name='unknown')
                        manufacturer_id = manufacturer.id
                    type = string.lower(row[3])

                    def f(x):
                        return {
                            'calculated': 0,
                            'sensor': 1,
                            'simulated': 2,
                            'derived': 3,
                        }.get(x, 1)
                    source_type = f(type)
                    details = row[4]
                    frequency = row[5]
                    timeout = row[6]
                    Source.objects.create(name=name,
                                          source_type=source_type,
                                          manufacturer_id=manufacturer_id,
                                          details=details,
                                          created=timezone.now(),
                                          uuid=uuid)
        print "completeted~!"
