from django.db import models

from .models import Timeseries

APP_LABEL = "ddsc_core"


class PiXml(models.Model):
    """Docstring"""
    header = models.TextField()
    timeseries = models.ForeignKey(Timeseries)

    class Meta:
        app_label = APP_LABEL
