from optparse import make_option

from django.core.management.base import BaseCommand
import pandas as pd

from tslib.readers import PiXmlReader
from tslib.writers import PiXmlWriter

from ddsc_core.models import Timeseries


class Command(BaseCommand):
    args = "<pi.xml>"
    help = (
        "Create pi.xml from a template. A template is a valid pi.xml file " +
        "without events (they are ignored if present) and per series a " +
        "`comment` element containing a ddsc timeseries uuid."
    )
    option_list = BaseCommand.option_list + (
        make_option(
            '-f',
            '--file',
            dest='file',
            help='write to file instead of stdout'
        ),
    )

    def handle(self, *args, **options):

        # source is a pi.xml file that serves as a template: its headers are
        # used, but any events are ignored. The `comment` element of each
        # series is expected to contain a ddsc uuid.

        try:
            source = args[0]
        except IndexError:
            self.stderr.write(self.help)
            return

        # destination is the resulting pi.xml file. If no destination is
        # given, output is written to stdout.

        try:
            destination = open(options.get('file'), 'w')
        except TypeError:
            destination = self.stdout

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

        writer.write(destination)
