from django.core.management.base import BaseCommand
from ddsc_core.models.models import Timeseries


class Command(BaseCommand):
    help = '1.    Visits every timeserie\n \
      2.    Checks the dataset to which the timeserie belongs\n \
      3.    Checks the owner of the dataset\n \
      4.    Sets the owner of the timeserie to the owner of the dataset'

    def handle(self, *args, **options):
        for ts in Timeseries.objects.all():
            dt_set_list = ts.data_set.values()
            for ds in dt_set_list:
                data_set_id = ds['id']
                data_set_name = ds['name']
                data_owner_id = ds['owner_id']
            if ts.onwer_id == None:
                ts.owner_id = data_owner_id
                ts.save()
        print "all completeted~!"
