from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from pytz import timezone
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
        make_option(
            '-z',
            '--timezone',
            default='UTC',
            dest='tz',
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
        # given, output is written to stdout. Allow for strftime based
        # formatting of the filename. See: http://docs.python.org/2/
        # library/datetime.html#strftime-strptime-behavior

        try:
            utcnow = timezone('UTC').localize(datetime.utcnow())
            tznow = utcnow.astimezone(timezone(options.get('tz')))
            filename = tznow.strftime(options.get('file'))
            destination = open(filename, 'w')
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
