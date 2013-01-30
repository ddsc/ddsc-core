#from adaptor.model import CsvDbModel
from django.core.management.base import BaseCommand

#from ddsc_core.models import Location


#class MyCsvModel(CsvDbModel):
#
#    class Meta:
#        dbModel = Location
#        delimiter = ","


class Command(BaseCommand):
    args = '<CSV file>'
    help = 'Imports a CSV file of locations into the database.'

    def handle(self, *args, **options):
        self.stdout.write('Foobar "%s"' % 1)
