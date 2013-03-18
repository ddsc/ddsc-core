from ast import literal_eval
from datetime import datetime
from datetime import timedelta
from optparse import make_option
import logging

from django.core.management.base import BaseCommand
from pytz import timezone
import pandas as pd

from tslib.readers import PiXmlReader
from tslib.writers import PiXmlWriter

from ddsc_core.models import Timeseries

logger = logging.getLogger(__name__)
ISO8601 = "%Y-%m-%dT%H:%M:%SZ"


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
            dest='timezone',
        ),
        make_option(
            '-s',
            '--start',
            dest='start',
        ),
        make_option(
            '-e',
            '--end',
            dest='end',
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
            tznow = utcnow.astimezone(timezone(options.get('timezone')))
            filename = tznow.strftime(options.get('file'))
            destination = open(filename, 'w')
        except TypeError:
            destination = self.stdout

        # To limit the events to be returned, `start` and `end` can be used.
        # They can either be expressed as an ISO 8601 UTC datetime string
        # or as a timedelta relative to now, for example:
        #
        # --start=2012-01-01T00:00:00Z --end=2013-01-01T00:00:00Z
        # --start="{'days': -7}" --end="{}"

        start = options.get('start')

        if start is not None:
            try:
                start = datetime.strptime(start, ISO8601)
            except:
                try:
                    start = utcnow + timedelta(**literal_eval(start))
                except:
                    logger.error("Cannot parse option `start`")
                    start = None

        end = options.get('end')

        if end is not None:
            try:
                end = datetime.strptime(end, ISO8601)
            except:
                try:
                    end = utcnow + timedelta(**literal_eval(end))
                except:
                    logger.error("Cannot parse option `end`")
                    end = None

        reader = PiXmlReader(source)
        writer = PiXmlWriter(reader.get_tz())

        for md, _ in reader.get_series():

            try:
                uuid = md.pop('comment')
                timeseries = Timeseries.objects.get(uuid=uuid)
                df = timeseries.get_events(start=start, end=end)
                writer.set_series(md, df)
            except Timeseries.DoesNotExist:
                logger.warning("Timeseries {0} does not exist".format(uuid))
                df = pd.DataFrame()
                writer.set_series(md, df)
            except Exception as e:
                logger.error(e)

        writer.write(destination)
