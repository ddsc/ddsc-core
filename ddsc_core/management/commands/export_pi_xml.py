import sys

from django.core.management.base import BaseCommand
import pandas as pd

from tslib.readers import PiXmlReader
from tslib.writers import PiXmlWriter

from ddsc_core.models import Timeseries


class Command(BaseCommand):
    args = "<pi.xml>"
    help = "help"

    def handle(self, *args, **options):

        try:
            source = args[0]
        except IndexError:
            self.stdout.write(self.help)
            return

        reader = PiXmlReader(source)
        writer = PiXmlWriter(reader.get_tz())

        for md, _ in reader.get_series():

            try:
                uuid = md.pop('comment')
                timeseries = Timeseries.objects.get(uuid=uuid)
                df = timeseries.get_events()
                writer.set_series(md, df)
            except Timeseries.DoesNotExist:
                df = pd.DataFrame()
                writer.set_series(md, df)
            except:
                pass

        writer.write(sys.stdout)
